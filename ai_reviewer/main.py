from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from github import Github, Auth
import os
import json
import subprocess
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

# --- Environment Validation ---
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "ASSISTANT_ID",
    "GH_APP_ID",
    "GH_INSTALL_ID",
    "GH_WEBHOOK_SECRET",
    "GH_APP_KEY_PATH"
]

if missing_vars := [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]:
    missing = ", ".join(missing_vars)
    raise RuntimeError(f"❌ Missing required environment variables: {missing}")

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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- GitHub Auth via App Installation ---


def get_github():
    with open(GH_APP_KEY_PATH) as key_file:
        private_key = key_file.read()
    auth = Auth.AppAuth(
        app_id=GH_APP_ID,
        private_key=private_key,
    )
    install_token = auth.get_installation_access_token(GH_INSTALL_ID)
    return Github(install_token.token)

# --- Tool Call Execution ---


def execute(tool, args):
    gh = get_github()
    repo = gh.get_repo(REPO_FULL)

    if tool == "list_repo":
        contents = repo.get_contents("")
        return json.dumps([item.path for item in contents])

    elif tool == "get_file":
        file = repo.get_contents(args["path"])
        return file.decoded_content.decode()

    elif tool == "run_tests":
        result = subprocess.run(
            ["pytest", "-q"], capture_output=True, text=True)
        return result.stdout + result.stderr

    elif tool == "create_branch_pr":
        title, body, diff = args["title"], args["body"], args["diff"]
        branch = "ai-" + os.urandom(4).hex()
        base_sha = repo.get_branch("main").commit.sha
        repo.create_git_ref(ref=f"refs/heads/{branch}", sha=base_sha)
        pr = repo.create_pull(title=title, body=body, head=branch, base="main")
        return pr.html_url

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
            thread_id=thread_id,
            role="user",
            content=message
        )

        run = ai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        while run.status in ("queued", "in_progress", "requires_action"):
            run = ai.beta.threads.runs.retrieve(run.id, thread_id=thread_id)

            if run.status == "requires_action":
                call = run.required_action.submit_tool_outputs.tool_calls[0]
                result = execute(call.name, call.arguments)

                ai.beta.threads.runs.actions.submit(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": call.id,
                        "output": result
                    }]
                )

        messages = ai.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value

        return JSONResponse({"answer": response, "thread_id": thread_id}) # Test for reviwer1

    except Exception as e:
        print(f"🔥 Error in /api/chat: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

# --- GitHub Webhook Endpoint ---


@app.post("/github/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    payload = await request.body()
    secret = GH_WEBHOOK_SECRET.encode()
    expected_sig = "sha256=" + \
        hmac.new(secret, payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_sig, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")

    event = await request.json()
    action = event.get("action")
    event_type = request.headers.get("X-GitHub-Event")

    print(f"🔔 GitHub Event: {event_type} | Action: {action}")

    if event_type == "pull_request" and action == "opened":
        pr = event.get("pull_request", {})
        pr_title = pr.get("title")
        pr_url = pr.get("html_url")
        pr_user = pr.get("user", {}).get("login")
        pr_number = pr.get("number")

        message = f"""A new PR was opened by {pr_user}: {pr_title}
{pr_url}
Review the code and suggest improvements."""

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

                ai.beta.threads.runs.actions.submit(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": call.id,
                        "output": result
                    }]
                )

        messages = ai.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value

        gh = get_github()
        repo = gh.get_repo(REPO_FULL)
        repo.create_issue_comment(
            pr_number,
            f"🤖 **Pink Book AI Review:**\n\n{response}"
        )

    return JSONResponse({"status": "Webhook received and processed."})
