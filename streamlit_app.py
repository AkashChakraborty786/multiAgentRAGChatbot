import os

import requests
import streamlit as st

API_URL = os.getenv("CHATBOT_API_URL", "http://127.0.0.1:8001/chat")

st.set_page_config(page_title="Chatbot", page_icon="💬", layout="centered")
st.title("RAG Chatbot")
st.caption(f"Backend: `{API_URL}`")

if "messages" not in st.session_state:
    st.session_state.messages = []


def ask_backend(query: str) -> str:
    response = requests.post(
        API_URL,
        json={"query": query},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the knowledge base..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = ask_backend(prompt)
            except requests.exceptions.ConnectionError:
                reply = (
                    "Could not reach the API. Start FastAPI first:\n\n"
                    "`python -m uvicorn app.main:app --reload --port 8001`"
                )
            except requests.exceptions.HTTPError as exc:
                reply = f"API error ({exc.response.status_code}): {exc.response.text}"
            except requests.exceptions.RequestException as exc:
                reply = f"Request failed: {exc}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
