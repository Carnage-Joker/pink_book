import os
import random
import openai
from .utils.prompts import default_prompts  # Ensure this path is correct

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")


def generate_prompt():
    """Selects a random prompt from the default_prompts list."""
    return random.choice(default_prompts)


def generate_insight(journal_entry):
    """
    Generates an empathetic response to a journal entry.

    Parameters:
    - journal_entry (str): The user's journal entry.

    Returns:
    - str: A thoughtful, kind, and encouraging message.
    """
    # Define the system message
    system_message = {
        "role": "system",
        "content": (
            "You are a supportive and empathetic mental health assistant catering to the BDSM community. "
            "Read the following journal entry and respond with a thoughtful, kind, and encouraging message "
            "that helps the user reflect on their emotions and experiences relating to their sissification journey "
            "and/or sissy identity. Keep your response under 500 characters."
        )
    }

    # Define the user message
    user_message = {
        "role": "user",
        "content": f'Journal Entry: "{journal_entry}"\n\nResponse:'
    }

    # Create the chat completion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[system_message, user_message],
            max_tokens=150,  # Adjust to ensure the response is concise
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.7,
            presence_penalty=0.6
        )
    except Exception as e:
        raise RuntimeError(f"Error generating insight: {e}")

    # Extract the assistant's response
    insight = response.choices[0].message['content'].strip()

    # Ensure the insight is not too long
    max_length = 500  # Maximum character length
    if len(insight) > max_length:
        insight = insight[:max_length].rsplit(' ', 1)[0] + '...'

    return insight
