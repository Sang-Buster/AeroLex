import os
import sys
from pathlib import Path

import streamlit as st

# Add the project root directory to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure Streamlit page settings
st.set_page_config(
    page_title="AeroLex",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create data directories if they don't exist
os.makedirs("src/data/audio", exist_ok=True)
os.makedirs("src/data/text", exist_ok=True)


def main():
    # Sidebar
    with st.sidebar:
        # Logo placeholder
        favicon_path = str(project_root / "assets" / "favicon.png")
        st.image(favicon_path)

        # Title and subtitle
        st.title("AeroLex")
        st.caption("Making Airwaves Understandable")

        # Add some spacing
        st.markdown("---")

        # Copyright notice at the bottom of sidebar
        st.markdown("<br>" * 5, unsafe_allow_html=True)  # Add space
        st.caption("Copyright © Sang-Buster 2025-Present")

    # Main content area
    st.title("Welcome to AeroLex")
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
