import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Agri-LLM Hub", page_icon="🌾")
st.title("🌾 Agri-LLM Knowledge Hub")
st.markdown("### Expert Agricultural Advice & Market Insights")

# Sidebar for Confidence Score & Status
st.sidebar.header("System Status")
st.sidebar.info("Model: Llama-3-8B-Agent")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about crops, prices, or diseases..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for AI Response
    with st.chat_message("assistant"):
        st.markdown("Thinking...")