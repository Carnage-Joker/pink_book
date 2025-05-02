import streamlit as st
import requests

# Streamlit app for local AI reviewer GUI
st.set_page_config(page_title="Pink Book AI Reviewer", layout="wide")

# Backend API endpoint
API_URL = "http://localhost:3001/api/chat"

# Initialize session state


def init_state():
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = None
    if 'history' not in st.session_state:
        st.session_state.history = []


init_state()

st.title("Pink Book AI Reviewer")

# User input and send button
user_input = st.text_input("Enter your message:")
if st.button("Send"):
    if user_input and user_input.strip():
        payload = {
            "message": user_input,
            "thread_id": st.session_state.thread_id
        }
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "")
            st.session_state.thread_id = data.get("thread_id")

            # Append to history
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("AI", answer))
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI:** {msg}")

st.write("Use this interface to interact with the AI reviewer locally.")
