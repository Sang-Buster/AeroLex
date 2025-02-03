import os
from datetime import datetime

import streamlit as st

from components.sidebar import sidebar


def save_audio_file(audio_file):
    # Create a timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{timestamp}.wav"
    save_path = os.path.join("src/data/audio", filename)

    with open(save_path, "wb") as f:
        f.write(audio_file.getbuffer())
    return save_path


def audio_page():
    sidebar()

    st.markdown(
        "<h1 style='text-align: center;'>Audio Processing</h1>", unsafe_allow_html=True
    )

    # File upload section
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])

    if uploaded_file is not None:
        # Save the uploaded file
        save_path = save_audio_file(uploaded_file)
        st.success(f"File saved successfully at {save_path}")

        # Audio player
        st.audio(uploaded_file)

        # Waveform visualization placeholder
        st.subheader("Audio Waveform")
        st.info("Waveform visualization will be implemented here")

    # Audio recording section
    audio_recording = st.audio_input("Record a voice message")

    if audio_recording is not None:
        # Save the recorded audio
        save_path = save_audio_file(audio_recording)
        st.success(f"Recording saved successfully at {save_path}")

        # Audio player for recorded audio
        st.audio(audio_recording)

        # Visualization placeholder
        st.subheader("Recording Waveform")
        st.info("Waveform visualization will be implemented here")


if __name__ == "__main__":
    audio_page()
