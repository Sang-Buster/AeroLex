import os
from datetime import datetime

import streamlit as st

from components.audio_visualizer import (
    plot_3d_spectrogram,
    plot_melspectrogram,
    plot_spectrogram,
    plot_spectrum,
    plot_waveform,
)
from components.sidebar import sidebar
from utils.audio_processing import load_and_process_audio


def save_audio_file(audio_file):
    """Save uploaded audio file"""
    # Create a timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.wav"
    save_path = os.path.join("src/data/audio", filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

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

        # Load and process audio
        wav, sr = load_and_process_audio(save_path)

        # Visualization controls
        with st.expander("Visualization Settings", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                win_len = st.slider(
                    "Window Length (FFT size)",
                    min_value=512,
                    max_value=4096,
                    value=2048,
                    step=256,
                    help="Larger values give better frequency resolution but worse time resolution",
                )

                hop_len = st.slider(
                    "Hop Length",
                    min_value=win_len // 16,
                    max_value=win_len // 2,
                    value=win_len // 4,
                    step=win_len // 16,
                    help="Number of samples between successive frames",
                )

            with col2:
                n_mel = st.slider(
                    "Number of Mel Bands",
                    min_value=32,
                    max_value=256,
                    value=128,
                    step=8,
                    help="Number of Mel frequency bands",
                )

                ave_win_len = st.slider(
                    "Smoothing Window",
                    min_value=2,
                    max_value=500,
                    value=100,
                    step=2,
                    help="Window size for spectrum smoothing",
                )

        # Show current settings
        with st.expander("Current Settings", expanded=False):
            st.write(f"""
            - Sample Rate: {sr} Hz
            - Window Length: {win_len} samples ({win_len / sr * 1000:.1f} ms)
            - Hop Length: {hop_len} samples ({hop_len / sr * 1000:.1f} ms)
            - Time Resolution: {hop_len / sr * 1000:.1f} ms
            - Frequency Resolution: {sr / win_len:.1f} Hz
            - Number of Mel Bands: {n_mel}
            - Smoothing Window: {ave_win_len} points
            """)

        # Display visualizations
        st.plotly_chart(plot_waveform(wav, sr))
        st.plotly_chart(plot_spectrum(wav, sr, ave_win_len))
        st.plotly_chart(plot_spectrogram(wav, sr, win_len, hop_len))
        st.plotly_chart(plot_melspectrogram(wav, sr, win_len, hop_len, n_mel))
        st.plotly_chart(plot_3d_spectrogram(wav, sr, win_len, hop_len))

    # Audio recording section
    audio_recording = st.audio_input("Record a voice message")

    if audio_recording is not None:
        # Save the recorded audio
        save_path = save_audio_file(audio_recording)
        st.success(f"Recording saved successfully at {save_path}")

        # Audio player for recorded audio
        st.audio(audio_recording)

        # Load and process recorded audio
        wav, sr = load_and_process_audio(save_path)

        # Visualization controls for recording
        with st.expander("Recording Visualization Settings", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                rec_win_len = st.slider(
                    "Recording Window Length (FFT size)",
                    min_value=512,
                    max_value=4096,
                    value=2048,
                    step=256,
                    help="Larger values give better frequency resolution but worse time resolution",
                )

                rec_hop_len = st.slider(
                    "Recording Hop Length",
                    min_value=rec_win_len // 16,
                    max_value=rec_win_len // 2,
                    value=rec_win_len // 4,
                    step=rec_win_len // 16,
                    help="Number of samples between successive frames",
                )

            with col2:
                rec_n_mel = st.slider(
                    "Recording Number of Mel Bands",
                    min_value=32,
                    max_value=256,
                    value=128,
                    step=8,
                    help="Number of Mel frequency bands",
                )

                rec_ave_win_len = st.slider(
                    "Recording Smoothing Window",
                    min_value=2,
                    max_value=500,
                    value=100,
                    step=2,
                    help="Window size for spectrum smoothing",
                )

        # Show current settings for recording
        with st.expander("Recording Current Settings", expanded=False):
            st.write(f"""
            - Sample Rate: {sr} Hz
            - Window Length: {rec_win_len} samples ({rec_win_len / sr * 1000:.1f} ms)
            - Hop Length: {rec_hop_len} samples ({rec_hop_len / sr * 1000:.1f} ms)
            - Time Resolution: {rec_hop_len / sr * 1000:.1f} ms
            - Frequency Resolution: {sr / rec_win_len:.1f} Hz
            - Number of Mel Bands: {rec_n_mel}
            - Smoothing Window: {rec_ave_win_len} points
            """)

        # Display visualizations for recorded audio
        st.plotly_chart(plot_waveform(wav, sr))
        st.plotly_chart(plot_spectrum(wav, sr, rec_ave_win_len))
        st.plotly_chart(plot_spectrogram(wav, sr, rec_win_len, rec_hop_len))
        st.plotly_chart(
            plot_melspectrogram(wav, sr, rec_win_len, rec_hop_len, rec_n_mel)
        )
        st.plotly_chart(plot_3d_spectrogram(wav, sr, rec_win_len, rec_hop_len))


if __name__ == "__main__":
    audio_page()
