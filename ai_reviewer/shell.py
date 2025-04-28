import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

assistant = openai.beta.assistants.create(
    name="Pink Book Reviewer",
    model="gpt-4o",
    instructions="""
    You are a senior developer reviewing a Django + React project.
    Use tools to list files, read contents, propose diffs, and run tests.
    """,
    tools=[
        {"type": "function", "function": {"name": "list_repo", "parameters": {"type": "object", "properties": {}}}},
        {"type": "function", "function": {
            "name": "get_file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }}},
        {"type": "function", "function": {"name": "run_tests", "parameters": {"type": "object", "properties": {}}}},
        {"type": "function", "function": {
            "name": "create_branch_pr",
            "parameters": {
                "type": "object",
                "properties": {
                    "diff": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["diff", "title", "body"]
            }}}
    ]
)

print("✅ Assistant created.")
print("🆔 Assistant ID:", assistant.id)

# Save it to .env
with open(".env", "a") as f:
    f.write(f"\nASSISTANT_ID={assistant.id}\n")

print("✅ Assistant ID saved to .env")
