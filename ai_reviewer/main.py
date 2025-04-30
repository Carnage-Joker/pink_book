from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from github import Github, Auth
import os
import json
import subprocess
import hmac
import hashlib
import tempfile
from dotenv import load_dotenv

# Load environment variables
t = load_dotenv()

# --- Environment Validation ---
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "ASSISTANT_ID",
    "GH_APP_ID",
    "GH_INSTALL_ID",
    "GH_WEBHOOK_SECRET",
    "GH_APP_KEY_PATH",
    "LOCAL_REPO_PATH"
]
missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
if missing:
    raise RuntimeError(
        f"❌ Missing required environment variables: {', '.join(missing)}")

# --- Configuration ---
app = FastAPI()
ai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)
REPO_FULL = "carnage-joker/pink_book"
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
GH_WEBHOOK_SECRET = os.getenv("GH_WEBHOOK_SECRET")
GH_APP_KEY_PATH = os.getenv("GH_APP_KEY_PATH")
GH_INSTALL_ID = os.getenv("GH_INSTALL_ID")
GH_APP_ID = os.getenv("GH_APP_ID")
LOCAL_REPO_PATH = os.getenv("LOCAL_REPO_PATH")

# --- GitHub Auth via App Installation ---


def get_github():
    private_key = open(GH_APP_KEY_PATH).read()
    auth = Auth.AppAuth(app_id=GH_APP_ID, private_key=private_key)
    token = auth.get_installation_access_token(GH_INSTALL_ID).token
    return Github(token)

# --- Tool Call Execution ---


def execute(tool, args):
    # Local operations
    if tool == "list_local_repo":
        paths = []
        for root, _, files in os.walk(LOCAL_REPO_PATH):
            for f in files:
                p = os.path.relpath(os.path.join(root, f), LOCAL_REPO_PATH)
                paths.append(p)
        return json.dumps(paths)

    if tool == "get_local_file":
        path = args.get("path")
        full = os.path.join(LOCAL_REPO_PATH, path)
        with open(full, encoding="utf-8") as f:
            return f.read()

    if tool == "run_local_tests":
        cmd = ["pytest", "-q"]
        res = subprocess.run(cmd, cwd=LOCAL_REPO_PATH,
                             capture_output=True, text=True)
        return res.stdout + res.stderr

    if tool == "create_local_branch":
        diff = args.get("diff")
        title = args.get("title")
        branch = "ai-fix-local-" + os.urandom(4).hex()
        subprocess.run(["git", "-C", LOCAL_REPO_PATH,
                       "checkout", "-b", branch], check=True)
        proc = subprocess.Popen(
            ["git", "-C", LOCAL_REPO_PATH, "apply"], stdin=subprocess.PIPE, text=True)
        proc.communicate(diff)
        subprocess.run(["git", "-C", LOCAL_REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", LOCAL_REPO_PATH,
                       "commit", "-m", title], check=True)
        return branch

    # GitHub-based operations
    gh = get_github()
    repo = gh.get_repo(REPO_FULL)

    if tool == "list_repo":
        contents = repo.get_contents("")
        return json.dumps([item.path for item in contents])

    if tool == "get_file":
        file = repo.get_contents(args["path"])
        return file.decoded_content.decode()

    if tool == "run_tests":
        pattern = args.get("pattern", "")
        cmd = ["pytest", "-q"]
        if pattern:
            cmd.append(pattern)
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.stdout + res.stderr

    if tool == "create_branch_pr":
        diff = args["diff"]
        title = args["title"]
        body = args["body"]
        tmpdir = tempfile.mkdtemp()
        auth_app = Auth.AppAuth(
            app_id=GH_APP_ID, private_key=open(GH_APP_KEY_PATH).read())
        token = auth_app.get_installation_access_token(GH_INSTALL_ID).token
        repo_url = f"https://x-access-token:{token}@github.com/{REPO_FULL}.git"
        subprocess.run(["git", "clone", repo_url, tmpdir], check=True)
        branch = "ai-fix-" + os.urandom(4).hex()
        subprocess.run(["git", "-C", tmpdir, "checkout",
                       "-b", branch], check=True)
        p = subprocess.Popen(["git", "-C", tmpdir, "apply"],
                             stdin=subprocess.PIPE, text=True)
        p.communicate(diff)
        subprocess.run(["git", "-C", tmpdir, "add", "."], check=True)
        subprocess.run(
            ["git", "-C", tmpdir, "commit", "-m", title], check=True)
        subprocess.run(["git", "-C", tmpdir, "push",
                       "origin", branch], check=True)
        pr = repo.create_pull(title=title, body=body, head=branch, base="main")
        return pr.html_url

    if tool == "get_pr_diff":
        pr = repo.get_pull(args.get("pr_number"))
        return pr.diff_url or pr.patch_url

    if tool == "search_code":
        query = args.get("query")
        results = gh.search_code(query + f" repo:{REPO_FULL}")
        return json.dumps([item.path for item in results])

    if tool == "run_lint":
        res = subprocess.run(["flake8"], cwd=LOCAL_REPO_PATH,
                             capture_output=True, text=True)
        return res.stdout + res.stderr

    return "Unknown tool"

# --- Chat Endpoint ---


@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        thread_id = data.get("thread_id")
        if not thread_id:
            thread = ai.beta.threads.create()
            thread_id = thread.id
        ai.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message)
        run = ai.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=ASSISTANT_ID)
        while run.status in ("queued", "in_progress", "requires_action"):
            run = ai.beta.threads.runs.retrieve(run.id, thread_id=thread_id)
            if run.status == "requires_action":
                call = run.required_action.submit_tool_outputs.tool_calls[0]
                result = execute(call.name, call.arguments)
                ai.beta.threads.runs.actions.submit(thread_id=thread_id, run_id=run.id, tool_outputs=[
                                                    {"tool_call_id": call.id, "output": result}])
        msgs = ai.beta.threads.messages.list(thread_id=thread_id)
        return JSONResponse({"answer": msgs.data[0].content[0].text.value, "thread_id": thread_id})
    except Exception as e:
        print(f"🔥 Error in /api/chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- GitHub Webhook Endpoint ---


@app.post("/github/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    payload = await request.body()
    sig = hmac.new(GH_WEBHOOK_SECRET.encode(),
                   payload, hashlib.sha256).hexdigest()
    if f"sha256={sig}" != x_hub_signature_256:
        raise HTTPException(status_code=403, detail="Invalid signature")
    evt = await request.json()
    if evt.get("action") == "opened" and request.headers.get("X-GitHub-Event") == "pull_request":
        pr = evt["pull_request"]
        msg = f"A new PR by {pr['user']['login']}: {pr['title']}\n{pr['html_url']}"
        thread = ai.beta.threads.create()
        ai.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=msg)
        run = ai.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=ASSISTANT_ID)
        while run.status in ("queued", "in_progress", "requires_action"):
            run = ai.beta.threads.runs.retrieve(run.id, thread_id=thread.id)
            if run.status == "requires_action":
                call = run.required_action.submit_tool_outputs.tool_calls[0]
                res = execute(call.name, call.arguments)
                ai.beta.threads.runs.actions.submit(thread_id=thread.id, run_id=run.id, tool_outputs=[
                                                    {"tool_call_id": call.id, "output": res}])
        ans = ai.beta.threads.messages.list(
            thread_id=thread.id).data[0].content[0].text.value
        gh = get_github()
        repo = gh.get_repo(REPO_FULL)
        repo.create_issue_comment(
            pr.get("number"), f"🤖 **Pink Book AI Review:**\n\n{ans}")
    return JSONResponse({"status": "Webhook received and processed."})
