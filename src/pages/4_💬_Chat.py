import streamlit as st

from components.sidebar import sidebar


def llm_chat_page():
    sidebar()

    st.markdown("<h1 style='text-align: center;'>LLM Chat</h1>", unsafe_allow_html=True)
    st.info("LLM Chat functionality will be implemented here")


if __name__ == "__main__":
    llm_chat_page()
