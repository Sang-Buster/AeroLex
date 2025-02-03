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

    # Initialize session state
    if "uploaded_audio" not in st.session_state:
        st.session_state.uploaded_audio = None
        st.session_state.uploaded_path = None
        st.session_state.uploaded_wav = None
        st.session_state.uploaded_sr = None

    if "recorded_audio" not in st.session_state:
        st.session_state.recorded_audio = None
        st.session_state.recorded_path = None
        st.session_state.recorded_wav = None
        st.session_state.recorded_sr = None

    # File upload section
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])

    if uploaded_file is not None and uploaded_file != st.session_state.uploaded_audio:
        # Only save if it's a new file
        st.session_state.uploaded_audio = uploaded_file
        save_path = save_audio_file(uploaded_file)
        st.session_state.uploaded_path = save_path
        st.success(f"File saved successfully at {save_path}")

        # Load and process audio
        wav, sr = load_and_process_audio(save_path)
        st.session_state.uploaded_wav = wav
        st.session_state.uploaded_sr = sr

    if st.session_state.uploaded_audio is not None:
        # Audio player
        st.audio(st.session_state.uploaded_audio)

        # Visualization controls
        with st.expander("Visualization Settings", expanded=False):
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

        # Display visualizations
        st.plotly_chart(
            plot_waveform(st.session_state.uploaded_wav, st.session_state.uploaded_sr),
            key="upload_waveform",
        )
        st.plotly_chart(
            plot_spectrum(
                st.session_state.uploaded_wav, st.session_state.uploaded_sr, ave_win_len
            ),
            key="upload_spectrum",
        )
        st.plotly_chart(
            plot_spectrogram(
                st.session_state.uploaded_wav,
                st.session_state.uploaded_sr,
                win_len,
                hop_len,
            ),
            key="upload_spectrogram",
        )
        st.plotly_chart(
            plot_melspectrogram(
                st.session_state.uploaded_wav,
                st.session_state.uploaded_sr,
                win_len,
                hop_len,
                n_mel,
            ),
            key="upload_melspec",
        )
        st.plotly_chart(
            plot_3d_spectrogram(
                st.session_state.uploaded_wav,
                st.session_state.uploaded_sr,
                win_len,
                hop_len,
            ),
            key="upload_3d",
        )

    # Audio recording section
    st.markdown("---")
    audio_recording = st.audio_input("Record a voice message")

    if (
        audio_recording is not None
        and audio_recording != st.session_state.recorded_audio
    ):
        # Only save if it's a new recording
        st.session_state.recorded_audio = audio_recording
        save_path = save_audio_file(audio_recording)
        st.session_state.recorded_path = save_path
        st.success(f"Recording saved successfully at {save_path}")

        # Load and process recorded audio
        wav, sr = load_and_process_audio(save_path)
        st.session_state.recorded_wav = wav
        st.session_state.recorded_sr = sr

    if st.session_state.recorded_audio is not None:
        # Audio player for recorded audio
        st.audio(st.session_state.recorded_audio)

        # Visualization controls
        with st.expander("Recording Visualization Settings", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                rec_win_len = st.slider(
                    "Recording Window Length",
                    min_value=512,
                    max_value=4096,
                    value=2048,
                    step=256,
                    key="rec_win_len",
                )
                rec_hop_len = st.slider(
                    "Recording Hop Length",
                    min_value=rec_win_len // 16,
                    max_value=rec_win_len // 2,
                    value=rec_win_len // 4,
                    step=rec_win_len // 16,
                    key="rec_hop_len",
                )
            with col2:
                rec_n_mel = st.slider(
                    "Recording Mel Bands",
                    min_value=32,
                    max_value=256,
                    value=128,
                    step=8,
                    key="rec_n_mel",
                )
                rec_ave_win_len = st.slider(
                    "Recording Smoothing",
                    min_value=2,
                    max_value=500,
                    value=100,
                    step=2,
                    key="rec_ave_win",
                )

        # Display visualizations for recorded audio
        st.plotly_chart(
            plot_waveform(st.session_state.recorded_wav, st.session_state.recorded_sr),
            key="rec_waveform",
        )
        st.plotly_chart(
            plot_spectrum(
                st.session_state.recorded_wav,
                st.session_state.recorded_sr,
                rec_ave_win_len,
            ),
            key="rec_spectrum",
        )
        st.plotly_chart(
            plot_spectrogram(
                st.session_state.recorded_wav,
                st.session_state.recorded_sr,
                rec_win_len,
                rec_hop_len,
            ),
            key="rec_spectrogram",
        )
        st.plotly_chart(
            plot_melspectrogram(
                st.session_state.recorded_wav,
                st.session_state.recorded_sr,
                rec_win_len,
                rec_hop_len,
                rec_n_mel,
            ),
            key="rec_melspec",
        )
        st.plotly_chart(
            plot_3d_spectrogram(
                st.session_state.recorded_wav,
                st.session_state.recorded_sr,
                rec_win_len,
                rec_hop_len,
            ),
            key="rec_3d",
        )


if __name__ == "__main__":
    audio_page()
