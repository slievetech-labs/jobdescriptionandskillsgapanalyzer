import streamlit as st
from anthropic import Anthropic

client = Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-4-7",
)
print(message.content)