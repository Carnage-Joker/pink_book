import streamlit as st
import requests

# Streamlit app for local AI reviewer GUI
st.set_page_config(page_title="Pink Book AI Reviewer", layout="wide")

# Backend API endpoint
API_URL = "http://localhost:3001/api/chat"

# Initialize session state
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Pink Book AI Reviewer")

            data = res.json()
            answer = data.get("answer", "")
            st.session_state.thread_id = data.get("thread_id")

            # Append to history
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("AI", answer))
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
for speaker, message in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**AI:** {message}")

# Instruction
st.write("Use this interface to interact with the AI reviewer locally.")
