import streamlit as st
import requests
from typing import Any, Tuple

# Streamlit app for local AI reviewer GUI
st.set_page_config(page_title="Pink Book AI Reviewer", layout="wide")

# Backend API endpoint
API_URL = "http://localhost:3001/api/chat"

# Initialize session state
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'history' not in st.session_state:
    st.session_state.history: list[Tuple[str, str]] = []

st.title("Pink Book AI Reviewer")

# User input section
user_input = st.text_input("Enter your message:", key='input')
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a message before sending.")
    else:
        payload: dict[str, Any] = {
            "message": user_input,
            "thread_id": st.session_state.thread_id
        }
        try:
            res = requests.post(API_URL, json=payload)
            res.raise_for_status()
            data = res.json()
            answer = data.get('answer', '')
            st.session_state.thread_id = data.get('thread_id')

            # Append to history
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(
                ("AI", answer or "[no response received]"))
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
