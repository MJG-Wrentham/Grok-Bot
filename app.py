import streamlit as st
import json
import os
from openai import OpenAI

# === CONFIGURATION ===
st.set_page_config(page_title="Grok Bot with Memory", page_icon="🤖")

# Put your xAI Grok API key in Streamlit secrets later (or hardcode for testing)
client = OpenAI(
    api_key=st.secrets.get("XAI_API_KEY", "YOUR_API_KEY_HERE"),
    base_url="https://api.x.ai/v1"
)

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Load persistent history
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.title("🤖 Grok Bot – Persistent Memory")
st.caption("Conversations are saved and remembered across sessions.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask Grok anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Grok response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="grok-4",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                save_history(st.session_state.messages)  # Save to file
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar controls
with st.sidebar:
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        save_history([])
        st.rerun()
