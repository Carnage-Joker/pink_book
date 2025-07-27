from .utils.prompts import default_prompts  # adjust path as needed
import os
import random
import openai
from typing import Any
from .utils.prompts import default_prompts  # Ensure this path is correct
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY.")

# Pin to a stable model
CHAT_MODEL = "gpt-4-0613"


def generate_prompt() -> str:
    return random.choice(default_prompts)


def generate_insight(journal_entry: str) -> str:
    system = {
        "role": "system",
        "content": (
            "You are a supportive and empathetic mental health assistant. "
            "Provide a thoughtful, kind, and encouraging message under 500 characters."
        )
    }
    user = {
        "role": "user",
        "content": f"Journal Entry: {journal_entry}"
    }
    try:
        resp = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=[system, user],
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.7,
            presence_penalty=0.6
        )
        insight = resp.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Insight generation failed: {e}")

    if len(insight) > 500:
        insight = insight[:500].rsplit(' ', 1)[0] + '...'
    return insight


def check_content_topic_with_openai(entry_content: str, prompt_text: str) -> bool:
    system = {
        "role": "system",
        "content": (
            "You are a strict content verifier. "
            "Respond with 'Yes' or 'No' only."
        )
    }
    user = {
        "role": "user",
        "content": (
            f"Requirement: {prompt_text}\n\nJournal Entry: {entry_content}\nRespond with 'Yes' or 'No'."
        )
    }
    try:
        resp = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=[system, user],
            max_tokens=10,
            temperature=0.2
        )
        result = resp.choices[0].message.content.strip().lower()
        logger.info(f"Topic check result: {result}")
        return result.startswith('yes')
    except Exception as e:
        logger.error(f"Topic check failed: {e}")
        return False
