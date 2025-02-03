import os
import sys
from pathlib import Path

import streamlit as st

from components.sidebar import sidebar

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure Streamlit page settings
st.set_page_config(
    page_title="AeroLex",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Create data directories if they don't exist
os.makedirs("src/data/audio", exist_ok=True)
os.makedirs("src/data/text", exist_ok=True)


def main():
    sidebar()

    # Main content area
    st.markdown(
        "<h1 style='text-align: center;'>Welcome to AeroLex</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    AeroLex is an AI-powered web application that transcribes, visualizes, 
    and analyzes air traffic communication.
    
    Use the sidebar navigation to explore different features:
    - 🎵 **Audio**: Upload or record audio files
    - 📝 **Text**: Input or upload text
    - 📋 **Transcription**: View transcribed content
    - 💬 **LLM Chat**: Interact with AI analysis
    """)


if __name__ == "__main__":
    main()
