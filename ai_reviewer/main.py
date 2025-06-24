import os
import json
import subprocess
import tempfile
import hmac
import hashlib
from typing import Any, Dict, Optional, List

import requests
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from github import Github, GithubIntegration
from github.Repository import Repository
from dotenv import load_dotenv
import openai

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
GH_APP_ID_ENV = os.getenv("GH_APP_ID")
GH_INSTALL_ID_ENV = os.getenv("GH_INSTALL_ID")
GH_WEBHOOK_SECRET = os.getenv("GH_WEBHOOK_SECRET")
GH_APP_KEY_PATH = os.getenv("GH_APP_KEY_PATH")
LOCAL_REPO_PATH = os.getenv("LOCAL_REPO_PATH")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if GH_APP_ID_ENV is None or GH_INSTALL_ID_ENV is None:
    raise RuntimeError(
        "GH_APP_ID and GH_INSTALL_ID must be set in environment variables")
GH_APP_ID = int(GH_APP_ID_ENV)
GH_INSTALL_ID = int(GH_INSTALL_ID_ENV)


def get_github() -> Github:
    """Authenticate via GitHub App installation."""
    if GH_APP_KEY_PATH is None:
        raise RuntimeError("GH_APP_KEY_PATH is not set")
    try:
        with open(GH_APP_KEY_PATH, "r", encoding="utf-8") as f:
            key = f.read()
        integration = GithubIntegration(GH_APP_ID, key)
        token = integration.get_access_token(GH_INSTALL_ID).token
        return Github(token)
    except Exception as e:
        raise RuntimeError(f"GitHub authentication failed: {e}")


def _list_local_repo() -> str:
    if LOCAL_REPO_PATH is None or not os.path.isdir(LOCAL_REPO_PATH):
        raise RuntimeError(f"Invalid LOCAL_REPO_PATH: {LOCAL_REPO_PATH}")
    files: List[str] = []
    for root, _, names in os.walk(LOCAL_REPO_PATH):
        for name in names:
            files.append(
                os.path.relpath(os.path.join(root, name), LOCAL_REPO_PATH)
            )
    return json.dumps(files)


def _get_local_file(args: Dict[str, Any]) -> str:
    path = args.get("path", "")
    if LOCAL_REPO_PATH is None:
        raise RuntimeError("LOCAL_REPO_PATH is not set")
    full = os.path.join(LOCAL_REPO_PATH, path)
    if not os.path.isfile(full):
        raise RuntimeError(f"File not found: {full}")
    with open(full, encoding="utf-8") as f:
        return f.read()


def _run_local_tests() -> str:
    if LOCAL_REPO_PATH is None:
        raise RuntimeError("LOCAL_REPO_PATH is not set")
    res = subprocess.run(
        ["pytest", "-q"],
        cwd=LOCAL_REPO_PATH,
        capture_output=True,
        text=True
    )
    return res.stdout + res.stderr


def _create_local_branch(args: Dict[str, Any]) -> str:
    diff = args.get("diff", "")
    title = args.get("title", "AI commit")
    if LOCAL_REPO_PATH is None:
        raise RuntimeError("LOCAL_REPO_PATH is not set")
    branch = f"ai-fix-local-{os.urandom(4).hex()}"
    subprocess.run(
        ["git", "-C", LOCAL_REPO_PATH, "checkout", "-b", branch],
        check=True
    )
    p = subprocess.Popen(
        ["git", "-C", str(LOCAL_REPO_PATH), "apply"],
        stdin=subprocess.PIPE,
        text=True
    )
    p.communicate(diff)
    subprocess.run(
        ["git", "-C", LOCAL_REPO_PATH, "add", "."],
        check=True
    )
    subprocess.run(
        ["git", "-C", LOCAL_REPO_PATH, "commit", "-m", title],
        check=True
    )
    return branch


def execute_local(tool: str, args: Dict[str, Any]) -> Optional[str]:
    # Map of local tools to their corresponding functions.
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


def execute_remote(
    tool: str,
    repo: Repository,
    args: Dict[str, Any],
    gh: Github
) -> Optional[str]:
    if tool == "list_repo":
        items = repo.get_contents("")
        items = items if isinstance(items, list) else [items]
        return json.dumps([i.path for i in items])

    if tool == "get_file":
        path = args.get("path", "")
        f = repo.get_contents(path)
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
        if GH_APP_KEY_PATH is None:
            raise RuntimeError("GH_APP_KEY_PATH is not set")
        with open(GH_APP_KEY_PATH, "r", encoding="utf-8") as f:
            key = f.read()
        integration = GithubIntegration(GH_APP_ID, key)
        token = integration.get_access_token(GH_INSTALL_ID).token
        url = f"https://x-access-token:{token}@github.com/{REPO_FULL}.git"
        subprocess.run(["git", "clone", url, td], check=True)
        branch = f"ai-fix-{os.urandom(4).hex()}"
        subprocess.run(["git", "-C", td, "checkout", "-b", branch], check=True)
        p = subprocess.Popen(
            ["git", "-C", td, "apply"],
            stdin=subprocess.PIPE,
            text=True
        )
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
        if LOCAL_REPO_PATH is None:
            raise RuntimeError("LOCAL_REPO_PATH is not set")
        res = subprocess.run(
            ["flake8"],
            cwd=LOCAL_REPO_PATH,
            capture_output=True,
            text=True
        )
        return res.stdout + res.stderr

    return None


def get_assistant_reply(thread_id: str) -> str:
    msgs = ai.beta.threads.messages.list(thread_id=thread_id).data
    last = msgs[-1].content[0]
    if getattr(last, "type", None) == "text":
        text = getattr(last, "text", None)
        return text.value if text and hasattr(text, "value") else "[No text value]"
    return str(last)


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
    # No-op: actual tool call handling would go here

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
        msg = (
            f"New PR by {pr['user']['login']}: {pr['title']}\n"
            f"{pr['html_url']}"
        )
        tid = ai.beta.threads.create().id
        ai.beta.threads.messages.create(
            thread_id=tid, role="user", content=msg
        )
        run = ai.beta.threads.runs.create(
            thread_id=tid, assistant_id=ASSISTANT_ID
        )
        process_tool_calls(tid, run)
        ans = get_assistant_reply(tid)
        gh = get_github()
        repo = gh.get_repo(REPO_FULL)
        repo.get_pull(pr["number"]).create_issue_comment(
            f"🤖 **AI Review:**\n\n{ans}"
        )

    # Ignore other event types (e.g., security_advisory) gracefully
    return JSONResponse({"status": "OK"})
