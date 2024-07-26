# generate.py
from transformers import pipeline

# Initialize the text generation pipeline with GPT-2
generator = pipeline("text-generation", model="gpt2")


def generate_prompt():
    prompt_text = "Write about a memorable experience."
    # Add truncation=True to handle long inputs properly
    generated = generator(prompt_text, max_length=50,
                          num_return_sequences=1, truncation=True)
    return generated['generated_text']


def generate_insight(entry_content):
    prompt_text = f"Provide an insightful comment on the following journal entry: {
        entry_content}"
    # Add truncation=True and set pad_token_id to avoid warnings
    generated = generator(prompt_text, max_length=50,
                          num_return_sequences=1, truncation=True, pad_token_id=50256)
    return generated[0]['generated_text']


if __name__ == "__main__":
    print("Prompt: ", generate_prompt())
    print("Insight: ", generate_insight(
        "Today I went to the park and saw beautiful flowers."))
