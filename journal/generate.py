import openai
import random
import os

from .utils.prompts import default_prompts  # Import the list from prompts.py


def generate_prompt():
    return random.choice(default_prompts)  # Return a random prompt from the list


# Make sure to set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_insight(journal_entry):
    prompt = f'You are a supportive and empathetic mental health assistant who caters to the bdsm community. Read the following journal entry and respond with a thoughtful, kind, and encouraging message that helps the user reflect on their emotions and experiences.\n\nJournal Entry: \"{journal_entry}\"\n\nResponse:'

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a supportive and empathetic mental health assistant catering to the bdsm community. Read the following journal entry and respond with a thoughtful, kind, and encouraging message that helps the user reflect on their emotions and experiences relating to their sissification journey and/or sissy identity. Keep your response under 500 characters"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,  # Adjust to ensure it's not too long
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.7,
        presence_penalty=0.6,
    )

    insight = response.choices[0].message['content'].strip()

    # Ensure the insight is not too long
    max_length = 500  # Set the desired max length for the insight
    if len(insight) > max_length:
        insight = insight[:max_length].rsplit(' ', 1)[0] + '...'

    return insight
