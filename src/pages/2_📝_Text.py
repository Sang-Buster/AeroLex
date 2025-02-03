import os
from datetime import datetime

import streamlit as st

from components.sidebar import sidebar


def save_text_file(text_content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"text_{timestamp}.txt"
    save_path = os.path.join("src/data/text", filename)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text_content)
    return save_path


def text_page():
    sidebar()

    st.markdown(
        "<h1 style='text-align: center;'>Text Processing</h1>", unsafe_allow_html=True
    )

    # File upload section
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        save_path = save_text_file(content)
        st.success(f"File saved successfully at {save_path}")

        # Display text content
        st.text_area("File Content", content, height=200)

        # Text visualization placeholder
        st.subheader("Text Analysis")
        st.info("Text analysis visualization will be implemented here")

    # Manual text input section
    text_input = st.text_area("Enter your text here", height=200)

    if st.button("Process Text") and text_input:
        save_path = save_text_file(text_input)
        st.success(f"Text saved successfully at {save_path}")

        # Text visualization placeholder
        st.subheader("Text Analysis")
        st.info("Text analysis visualization will be implemented here")


if __name__ == "__main__":
    text_page()
