# model_loader.py``
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
# model_loader.py
from gradio_client import Client

# Initialize the Gradio client
gradio_client = Client("Aarifkhan/NSFW-3B")

try:
    tokenizer = AutoTokenizer.from_pretrained(
        "zxbsmk/NSFW_13B_sft", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        "zxbsmk/NSFW_13B_sft", trust_remote_code=True)
except Exception as e:
    print(f"Error loading tokenizer and model: {e}")
    tokenizer = None
    model = None
