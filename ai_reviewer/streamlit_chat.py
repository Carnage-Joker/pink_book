import os
import streamlit as st
import requests
from typing import Any, Tuple

# Configuration: allow override via environment variable
API_URL = os.getenv("API_URL", "http://localhost:3001/api/chat")

# Persistent HTTP session for connection reuse
session = requests.Session()

# Streamlit app setup
st.set_page_config(page_title="Pink Book AI Reviewer", layout="wide")

# Initialize state
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'history' not in st.session_state:
    st.session_state.history: list[Tuple[str, str]] = []

st.title("Pink Book AI Reviewer")

# Chat input form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Enter your message:", key='input')
    submit = st.form_submit_button("Send")
    if submit:
        if not user_input.strip():
            st.warning("Please enter a message before sending.")
        else:
            payload: dict[str, Any] = {
                "message": user_input,
                "thread_id": st.session_state.thread_id
            }
            try:
                with st.spinner("Contacting AI..."):
                    response = session.post(API_URL, json=payload)
                    response.raise_for_status()
                data = response.json()
                answer = data.get('answer', '')
                st.session_state.thread_id = data.get('thread_id')

                # Update history
                st.session_state.history.append(("You", user_input))
                st.session_state.history.append(
                    ("AI", answer or "[no response received]"))

                # Trim history to last 100 entries to keep UI snappy
                if len(st.session_state.history) > 100:
                    st.session_state.history = st.session_state.history[-100:]
            except requests.RequestException as e:
                st.error(f"Error contacting API: {e}")

# Display chat history
if st.session_state.history:
    st.markdown("---")
    for speaker, msg in st.session_state.history:
        prefix = "**You:**" if speaker == "You" else "**AI:**"
        st.markdown(f"{prefix} {msg}")

st.markdown("---")
st.markdown(
    "Interact with the Pink Book AI reviewer. Messages will appear above.")
