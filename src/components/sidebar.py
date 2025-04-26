import sys
from pathlib import Path

import streamlit as st

# Add the project root directory to the Python path
src_root = Path(__file__).parent.parent
sys.path.insert(0, str(src_root))


def sidebar():
    # Sidebar
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)

        # Logo placeholder
        favicon_path = str(src_root / "assets" / "favicon.png")
        st.image(favicon_path, use_container_width=True)

        # Title and subtitle
        st.markdown(
            "<h1 style='text-align: center;'>AeroLex</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center;'>Making Airwaves Understandable</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h6 style='text-align: center;'> An AI-powered ATC Communication Analysis Tool</h6>",
            unsafe_allow_html=True,
        )

        # Footer
        st.markdown("<br>" * 7, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
            "<h6 style='text-align: center;'>Copyright © Sang-Buster 2025-Present</h6>",
            unsafe_allow_html=True,
        )
