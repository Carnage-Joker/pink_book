import openai
import random
import os

from .utils.prompts import default_prompts  # Import the list from prompts.py


def generate_prompt():
    return random.choice(default_prompts)  # Return a random prompt from the list


# Make sure to set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_insight(journal_entry):
    prompt = (
        "You are a supportive and empathetic mental health assistant. "
        "Read the following journal entry and respond with a thoughtful, kind, and encouraging message that helps the user reflect on their emotions and experiences.\n\n"
        "Journal Entry: \"{}\"\n\n"
        "Response:".format(journal_entry)
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a supportive and empathetic mental health assistant. Read the following journal entry and respond with a thoughtful, kind, and encouraging message that helps the user reflect on their emotions and experiences relating to their sissification journey and/or sissy identity."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # Adjust to ensure it's not too long
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    insight = response.choices[0].message['content'].strip()

    # Ensure the insight is not too long
    max_length = 250  # Set the desired max length for the insight
    if len(insight) > max_length:
        insight = insight[:max_length].rsplit(' ', 1)[0] + '...'

    return insight
