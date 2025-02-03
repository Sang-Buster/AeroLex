import streamlit as st

from components.sidebar import sidebar


def transcription_page():
    sidebar()

    st.markdown(
        "<h1 style='text-align: center;'>Transcription</h1>", unsafe_allow_html=True
    )
    st.info("Transcription functionality will be implemented here")


if __name__ == "__main__":
    transcription_page()
