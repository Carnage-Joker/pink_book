from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import openai
from github import Github, GithubIntegration
from github.Repository import Repository
import os
import json
import subprocess
import tempfile
import hmac
import hashlib
import requests
from dotenv import load_dotenv
from typing import Any, Dict, Optional, List

# Load & validate environment
load_dotenv()
REQUIRED = [
    "OPENAI_API_KEY", "ASSISTANT_ID",
    "GH_APP_ID", "GH_INSTALL_ID", "GH_WEBHOOK_SECRET", "GH_APP_KEY_PATH",
    "LOCAL_REPO_PATH"
]
missing = [v for v in REQUIRED if not os.getenv(v)]
if missing:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

# Config
app = FastAPI()
ai = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)
REPO_FULL = os.getenv("REPO_FULL", "carnage-joker/pink_book")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
GH_APP_ID = int(os.getenv("GH_APP_ID"))
GH_INSTALL_ID = int(os.getenv("GH_INSTALL_ID"))
GH_WEBHOOK_SECRET = os.getenv("GH_WEBHOOK_SECRET")
GH_APP_KEY_PATH = os.getenv("GH_APP_KEY_PATH")
LOCAL_REPO_PATH = os.getenv("LOCAL_REPO_PATH")


def get_github() -> Github:
    """Authenticate via GitHub App installation."""
    try:
        key = open(GH_APP_KEY_PATH, "r").read()
        integration = GithubIntegration(GH_APP_ID, key)
        token = integration.get_access_token(GH_INSTALL_ID).token
        return Github(token)
    except FileNotFoundError:
        raise RuntimeError(f"Key file not found: {GH_APP_KEY_PATH}")
    except Exception as e:
        raise RuntimeError(f"GitHub auth failed: {e}")


# --- Local tool implementations ---

def _list_local_repo() -> str:
    if not os.path.isdir(LOCAL_REPO_PATH):
        raise RuntimeError(f"Invalid LOCAL_REPO_PATH: {LOCAL_REPO_PATH}")
    files: List[str] = []
    for root, _, names in os.walk(LOCAL_REPO_PATH):
        for name in names:
            files.append(os.path.relpath(
                os.path.join(root, name), LOCAL_REPO_PATH))
    return json.dumps(files)


def _get_local_file(args: Dict[str, Any]) -> str:
    path = args.get("path", "")
    full = os.path.join(LOCAL_REPO_PATH, path)
    if not os.path.isfile(full):
        raise RuntimeError(f"File not found: {full}")
    return open(full, encoding="utf-8").read()


def _run_local_tests() -> str:
    res = subprocess.run(["pytest", "-q"], cwd=LOCAL_REPO_PATH,
                         capture_output=True, text=True)
    return res.stdout + res.stderr


def _create_local_branch(args: Dict[str, Any]) -> str:
    diff = args.get("diff", "")
    title = args.get("title", "AI commit")
    branch = f"ai-fix-local-{os.urandom(4).hex()}"
    subprocess.run(["git", "-C", LOCAL_REPO_PATH,
                   "checkout", "-b", branch], check=True)
    p = subprocess.Popen(["git", "-C", LOCAL_REPO_PATH,
                         "apply"], stdin=subprocess.PIPE, text=True)
    p.communicate(diff)
    subprocess.run(["git", "-C", LOCAL_REPO_PATH, "add", "."], check=True)
    subprocess.run(["git", "-C", LOCAL_REPO_PATH,
                   "commit", "-m", title], check=True)
    return branch


def execute_local(tool: str, args: Dict[str, Any]) -> Optional[str]:
    # Map of local tools to their corresponding functions.
    # - "list_local_repo": Lists all files in the local repository.
    # - "get_local_file": Retrieves the content of a specific file from the local repository.
    # - "run_local_tests": Executes local tests using pytest and returns the results.
    # - "create_local_branch": Creates a new local branch and applies a diff to it.
    locals_map = {
        "list_local_repo": _list_local_repo,
        "get_local_file": lambda: _get_local_file(args),
        "run_local_tests": _run_local_tests,
        "create_local_branch": lambda: _create_local_branch(args),
    }
    fn = locals_map.get(tool)
    if not fn:
        raise ValueError(f"Unknown local tool: {tool}")
    return fn()


# --- Remote tool implementations ---

def execute_remote(tool: str, repo: Repository, args: Dict[str, Any], gh: Github) -> Optional[str]:
    if tool == "list_repo":
        items = repo.get_contents("")
        items = items if isinstance(items, list) else [items]
        return json.dumps([i.path for i in items])

    if tool == "get_file":
        f = repo.get_contents(args["path"])
        if isinstance(f, list):
            return json.dumps([file.path for file in f])
        return f.decoded_content.decode("utf-8")

    if tool == "run_tests":
        res = subprocess.run(["pytest", "-q"], capture_output=True, text=True)
        return res.stdout + res.stderr

    if tool == "create_branch_pr":
        diff, title = args["diff"], args["title"]
        body = args.get("body", "")
        td = tempfile.mkdtemp()
        key = open(GH_APP_KEY_PATH, "r").read()
        integration = GithubIntegration(GH_APP_ID, key)
        token = integration.get_access_token(GH_INSTALL_ID).token
        url = f"https://x-access-token:{token}@github.com/{REPO_FULL}.git"
        subprocess.run(["git", "clone", url, td], check=True)
        branch = f"ai-fix-{os.urandom(4).hex()}"
        subprocess.run(["git", "-C", td, "checkout", "-b", branch], check=True)
        p = subprocess.Popen(["git", "-C", td, "apply"],
                             stdin=subprocess.PIPE, text=True)
        p.communicate(diff)
        subprocess.run(["git", "-C", td, "add", "."], check=True)
        subprocess.run(["git", "-C", td, "commit", "-m", title], check=True)
        subprocess.run(["git", "-C", td, "push", "origin", branch], check=True)
        pr = repo.create_pull(title=title, body=body, head=branch, base="main")
        return pr.html_url

    if tool == "get_pr_diff":
        pr = repo.get_pull(args["pr_number"])
        return requests.get(pr.patch_url).text

    if tool == "search_code":
        q = args.get("query", "")
        results = gh.search_code(f"repo:{REPO_FULL} {q}")
        return json.dumps([r.path for r in results])

    if tool == "run_lint":
        res = subprocess.run(["flake8"], cwd=LOCAL_REPO_PATH,
                             capture_output=True, text=True)
        return res.stdout + res.stderr

    return None


def execute(tool: str, args: Dict[str, Any]) -> str:
    local_out = execute_local(tool, args)
    if local_out is not None:
        return local_out
    gh = get_github()
    repo = gh.get_repo(REPO_FULL)
    remote_out = execute_remote(tool, repo, args, gh)
    return remote_out or "Unknown tool"


# --- Chat & Webhook helpers ---

def validate_message(data: Dict[str, Any]) -> str:
    m = data.get("message")
    if not isinstance(m, str) or not m.strip():
        raise HTTPException(400, "'message' must be a non-empty string")
    return m.strip()


def get_or_create_thread(data: Dict[str, Any]) -> str:
    tid = data.get("thread_id")
    if not tid:
        tid = ai.beta.threads.create().id
    return str(tid)


def process_tool_calls(thread_id: str, run: Any):
    while run.status in ("queued", "in_progress", "requires_action"):
        run = ai.beta.threads.runs.retrieve(run.id, thread_id=thread_id)
        if run.status != "requires_action":
            continue
        call = run.required_action.submit_tool_outputs.tool_calls[0].dict()
        out = execute(call["tool"], call["arguments"])
        ai.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=[{"tool_call_id": call["id"], "output": out}]
        )


def get_assistant_reply(thread_id: str) -> str:
    msgs = ai.beta.threads.messages.list(thread_id=thread_id).data
    last = msgs[-1].content[0]
    if getattr(last, "type", None) == "text":
        text = getattr(last, "text", None)
        return text.value if text and hasattr(text, "value") else "[No text value]"
    return str(last)


# --- API Endpoints ---

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    msg = validate_message(data)
    tid = get_or_create_thread(data)

    ai.beta.threads.messages.create(thread_id=tid, role="user", content=msg)
    run = ai.beta.threads.runs.create(thread_id=tid, assistant_id=ASSISTANT_ID)
    process_tool_calls(tid, run)
    ans = get_assistant_reply(tid)

    return JSONResponse({"answer": ans, "thread_id": tid})


@app.post("/github/webhook")
async def webhook(request: Request, x_hub_signature_256: str = Header(None)):
    raw = await request.body()
    if not GH_WEBHOOK_SECRET:
        raise HTTPException(500, "GH_WEBHOOK_SECRET is not set")
    sig = hmac.new(GH_WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if f"sha256={sig}" != x_hub_signature_256:
        raise HTTPException(403, "Invalid signature")

    evt = await request.json()
    event_type = request.headers.get("X-GitHub-Event")

    # Handle Pull Request opened
    if event_type == "pull_request" and evt.get("action") == "opened":
        pr = evt["pull_request"]
        msg = f"New PR by {pr['user']['login']}: {pr['title']}\n{pr['html_url']}"
        tid = ai.beta.threads.create().id
        ai.beta.threads.messages.create(
            thread_id=tid, role="user", content=msg)
        run = ai.beta.threads.runs.create(
            thread_id=tid, assistant_id=ASSISTANT_ID)
        process_tool_calls(tid, run)
        ans = get_assistant_reply(tid)
        gh = get_github()
        repo = gh.get_repo(REPO_FULL)
        repo.get_pull(pr["number"]).create_issue_comment(
            f"🤖 **AI Review:**\n\n{ans}")

    # Ignore other event types (e.g., security_advisory) gracefully
    return JSONResponse({"status": "OK"})
