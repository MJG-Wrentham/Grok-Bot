import streamlit as st
from openai import OpenAI

st.title("💬 Grok Chatbot")
st.caption("Powered by xAI Grok")

# Get xAI API key
xai_api_key = st.text_input("xAI API Key", type="password")
if not xai_api_key:
    st.info("Please add your xAI API key to continue. Get one at console.x.ai", icon="🗝️")
    st.stop()

client = OpenAI(
    api_key=xai_api_key,
    base_url="https://api.x.ai/v1"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Grok anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        stream = client.chat.completions.create(
            model="grok-4.6",   # or "grok-4.7" for the latest
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

