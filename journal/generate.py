import os
import random
import openai
from .utils.prompts import default_prompts  # Ensure this path is correct
import logging

logger = logging.getLogger(__name__)

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
            model="gpt-4",  # Use the appropriate model
            messages=[system_message, user_message],
            max_tokens=150,  # Adjust to ensure the response is concise
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.7,
            presence_penalty=0.6
        )

        # Extract the assistant's response
        choices = response.get("choices", [])
        if choices and "message" in choices[0] and "content" in choices[0]["message"]:
            insight = choices[0]["message"]["content"].strip()
        else:
            raise RuntimeError("Unexpected response structure from OpenAI API")
    except Exception as e:
        raise RuntimeError(f"Error generating insight: {e}") from e

    # Extract the assistant's response
    insight = response

    # Ensure the insight is not too long
    max_length = 500  # Maximum character length
    if len(insight) > max_length:
        insight = insight[:max_length].rsplit(' ', 1)[0] + '...'

    return insight


# Set up logging
logger = logging.getLogger(__name__)


def check_content_topic_with_openai(entry_content, prompt_topic):
    """
    Sends the content of the entry to OpenAI's API to check if it stayed on topic.

    Args:
        entry_content (str): The content of the journal entry.
        prompt_topic (str): The topic the user is supposed to write about.

    Returns:
        bool: True if the content stayed on topic, False otherwise.
    """
    try:
        # Construct the messages for the chat model/
        messages = [
            {"role": "system", "content": "You are an assistant that checks if content adheres to a given topic."},
            {"role": "user", "content": (
                f"Analyze the following journal entry and determine if it adheres to the specified topic:\n\n"
                f"Topic: {prompt_topic}\n"
                f"Entry: {entry_content}\n\n"
                f"Respond with 'Yes' if the entry stays on topic, or 'No' if it does not."
            )}
        ]

        # Call the OpenAI ChatCompletion API for analysis
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Corrected model name
            messages=messages,
            max_tokens=500,
            temperature=0.2  # Low temperature for consistent output
        )

        # Extract the response and log it
        result = response.choices[0].message['content'].strip()
        logger.info(f"OpenAI response for topic check: {result}")

        # Interpret the response
        return result.lower() == 'yes'

    except openai.OpenAIError as e:
        logger.error(f"Error while sending content to OpenAI API: {str(e)}")
        return False
