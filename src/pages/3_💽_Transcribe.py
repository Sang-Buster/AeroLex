import os
from datetime import datetime
from typing import Dict

import ollama
import streamlit as st
import torch
import whisper

from components.sidebar import sidebar
from components.transcription_viewer import display_summary
from utils.summarize import OllamaSummarizer
from utils.transcribe import WhisperTranscriber


def get_whisper_models() -> Dict[str, str]:
    """Get available Whisper models and their sizes"""
    # Model sizes in millions of parameters (from official OpenAI documentation)
    model_sizes = {
        "tiny.en": 39,
        "tiny": 39,
        "base.en": 74,
        "base": 74,
        "small.en": 244,
        "small": 244,
        "medium.en": 769,
        "medium": 769,
        "large-v1": 1550,
        "large-v2": 1550,
        "large": 1550,
    }

    # Get available models
    available_models = whisper.available_models()

    # Create formatted model names with sizes
    whisper_models = {}
    for model in available_models:
        if model in model_sizes:
            size = model_sizes[model]
            if size >= 1000:
                size_str = f"{size / 1000:.1f}GB"
            else:
                size_str = f"{size}M"
            whisper_models[model] = f"{model.title()} ({size_str})"

    return whisper_models


def update_whisper_model():
    st.session_state.whisper_model = st.session_state.whisper_model_selectbox


def update_ollama_model():
    st.session_state.ollama_model = st.session_state.ollama_model_selectbox


def transcription_page():
    sidebar()

    st.markdown(
        "<h1 style='text-align: center;'>Real-Time Transcription & Summary</h1>",
        unsafe_allow_html=True,
    )

    # Initialize session state for transcription
    if "transcribing" not in st.session_state:
        st.session_state.transcribing = False
    if "transcription_audio" not in st.session_state:
        st.session_state.transcription_audio = None
    if "transcription_path" not in st.session_state:
        st.session_state.transcription_path = None
    # Initialize session state for model selections with defaults
    if "whisper_model" not in st.session_state:
        st.session_state.whisper_model = "tiny"
    if "ollama_model" not in st.session_state:
        st.session_state.ollama_model = None

    # Model Selection in two columns
    model_col1, model_col2 = st.columns(2)

    with model_col1:
        # Get available Whisper models
        whisper_models = get_whisper_models()

        # Get current index
        model_options = list(whisper_models.keys())
        current_index = 0
        if st.session_state.whisper_model in model_options:
            current_index = model_options.index(st.session_state.whisper_model)

        # Use the callback pattern with a unique key
        st.selectbox(
            "Whisper Model",
            options=model_options,
            format_func=lambda x: whisper_models[x],
            index=current_index,
            key="whisper_model_selectbox",
            on_change=update_whisper_model,
            help=(
                "Select Whisper model for transcription. "
                "Larger models are more accurate but slower. "
                f"Using CUDA: {torch.cuda.is_available()}"
            ),
        )

        # Display selected model for debugging
        st.caption(f"Selected model: {st.session_state.whisper_model}")

    with model_col2:
        # Ollama model selection with dynamic model list
        try:
            # Use get method with default fallback for secrets
            ollama_api_url = st.secrets.get("OLLAMA_API_URL", "http://localhost:11434")

            # Create client without the HEAD request check that was causing issues
            client = ollama.Client(host=ollama_api_url)

            try:
                response = client.list()

                # Extract model names and details
                available_models = []
                model_details = {}

                if hasattr(response, "models") and response.models:
                    for model in response.models:
                        available_models.append(model.model)
                        size_gb = model.size / (1024 * 1024 * 1024)  # Convert to GB
                        model_details[model.model] = f"{model.model} ({size_gb:.1f}GB)"

                if not available_models:
                    st.warning(
                        "No Ollama models found. Please download at least one model for summarization."
                    )
                    available_models = ["None"]
                    model_details = {"None": "No models available"}

            except Exception as api_error:
                st.error(f"Error fetching models from Ollama: {str(api_error)}")
                st.info("API connection succeeded but model list retrieval failed.")
                available_models = ["None"]
                model_details = {"None": "API Error"}

        except KeyError:
            # Handle case when OLLAMA_API_URL is not in secrets
            st.info(
                "OLLAMA_API_URL not found in secrets, using default localhost:11434"
            )
            try:
                client = ollama.Client(host="http://localhost:11434")
                response = client.list()
                # Rest of the code to handle response
                # Extract model names and details
                available_models = []
                model_details = {}

                if hasattr(response, "models") and response.models:
                    for model in response.models:
                        available_models.append(model.model)
                        size_gb = model.size / (1024 * 1024 * 1024)  # Convert to GB
                        model_details[model.model] = f"{model.model} ({size_gb:.1f}GB)"

                if not available_models:
                    st.warning(
                        "No Ollama models found. Please download at least one model for summarization."
                    )
                    available_models = ["None"]
                    model_details = {"None": "No models available"}
            except Exception as inner_e:
                st.error(f"Failed to connect to local Ollama API: {str(inner_e)}")
                st.info(
                    "Make sure Ollama is running locally or port forwarding is correctly set up."
                )
                available_models = ["None"]
                model_details = {"None": "Connection Error"}

        except Exception as e:
            error_msg = str(e)
            st.error(f"Failed to connect to Ollama API: {error_msg}")

            # Provide a single, clear instruction instead of multiple messages
            st.info(
                "Check that Ollama is running and accessible. For remote connections, verify your port forwarding setup (e.g., ssh -L 11434:remote:11434)."
            )

            available_models = ["None"]
            model_details = {"None": "Connection Error"}

        # Get current index for Ollama model
        ollama_index = 0
        if st.session_state.ollama_model in available_models:
            ollama_index = available_models.index(st.session_state.ollama_model)

        # Use callback pattern with unique key for Ollama model
        st.selectbox(
            "Summarization Model",
            options=available_models,
            format_func=lambda x: model_details.get(x, x),
            index=ollama_index,
            key="ollama_model_selectbox",
            on_change=update_ollama_model,
            help="Select the Ollama model for summarization",
        )

        # Display selected model for debugging
        st.caption(f"Selected model: {st.session_state.ollama_model}")

    # Check for audio from Audio page
    has_uploaded_audio = (
        hasattr(st.session_state, "uploaded_audio")
        and st.session_state.uploaded_audio is not None
    )
    has_recorded_audio = (
        hasattr(st.session_state, "recorded_audio")
        and st.session_state.recorded_audio is not None
    )

    # Audio source selection
    source_options = ["Upload New Audio", "Record New Audio"]
    if has_uploaded_audio:
        source_options.insert(0, "Use Uploaded Audio")
    if has_recorded_audio:
        source_options.insert(0, "Use Recorded Audio")

    audio_source = st.radio("Select Audio Source", source_options)

    # Handle audio source selection
    if audio_source == "Use Uploaded Audio":
        st.audio(st.session_state.uploaded_audio)
        st.session_state.transcription_audio = st.session_state.uploaded_audio
        st.session_state.transcription_path = st.session_state.uploaded_path

    elif audio_source == "Use Recorded Audio":
        st.audio(st.session_state.recorded_audio)
        st.session_state.transcription_audio = st.session_state.recorded_audio
        st.session_state.transcription_path = st.session_state.recorded_path

    elif audio_source == "Upload New Audio":
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=["wav", "mp3", "ogg"],
            key="transcription_upload",
        )
        if uploaded_file:
            st.audio(uploaded_file)
            st.session_state.transcription_audio = uploaded_file
            # Save file and get path
            from utils.audio_processing import save_audio_file

            save_path = save_audio_file(uploaded_file)
            st.session_state.transcription_path = save_path

    elif audio_source == "Record New Audio":
        audio_recording = st.audio_input("Record Audio")
        if audio_recording:
            st.audio(audio_recording)
            st.session_state.transcription_audio = audio_recording
            # Save recording and get path
            from utils.audio_processing import save_audio_file

            save_path = save_audio_file(audio_recording)
            st.session_state.transcription_path = save_path

    # Main transcription and summary section with containers
    if st.session_state.transcription_path:
        # Initialize transcriber and summarizer first
        transcriber = WhisperTranscriber(
            model_name=st.session_state.whisper_model,
            audio_path=st.session_state.transcription_path,
        )

        summarizer = OllamaSummarizer(model_name=st.session_state.ollama_model)

        # Center the control buttons using columns
        left_col, center_col, right_col = st.columns([1, 2, 1])

        with center_col:
            if not st.session_state.transcribing:
                if st.button("Start Transcribing", use_container_width=True):
                    st.session_state.transcribing = True
                    st.rerun()
            else:
                if st.button(
                    "Stop Transcribing", use_container_width=True, type="primary"
                ):
                    st.session_state.transcribing = False
                    from utils.transcribe import send_stop_signal

                    send_stop_signal()
                    if hasattr(transcriber, "cleanup"):
                        transcriber.cleanup()
                    st.rerun()

        # Start transcription if enabled
        if st.session_state.transcribing:
            # Create two columns with equal width for transcription and summary
            trans_col1, trans_col2 = st.columns(2)

            # Create containers with consistent styling
            with trans_col1:
                transcription_container = st.container(border=True, height=700)
                with transcription_container:
                    st.markdown("#### Live Transcription")
                    transcription_content = st.empty()

            with trans_col2:
                summary_container = st.container(border=True, height=700)
                with summary_container:
                    st.markdown("#### Live Summary")
                    summary_content = st.empty()

            # Process transcription and update containers
            for transcription in transcriber.start():
                # Update transcription
                with transcription_content:
                    st.markdown(
                        f"""
                        <div style="height: 500px; overflow-y: auto; padding: 10px;">
                            {transcription.replace("\n", "<br>")}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Update and save summary
                with summary_content:
                    summary = summarizer.summarize(transcription)
                    display_summary(summary)

            # Add download buttons after transcription is complete
            if not st.session_state.transcribing and os.path.exists(
                transcriber.transcription_path
            ):
                col1, col2 = st.columns(2)
                with col1:
                    with open(
                        transcriber.transcription_path, "r", encoding="utf-8"
                    ) as f:
                        st.download_button(
                            "Download Transcription",
                            f.read(),
                            file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                        )

                with col2:
                    if os.path.exists(summarizer.summary_path):
                        with open(summarizer.summary_path, "r", encoding="utf-8") as f:
                            st.download_button(
                                "Download Summary",
                                f.read(),
                                file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                            )
    else:
        st.info("Please select or upload an audio source to begin transcription")

    # Auto-start transcription when audio is ready
    if (
        st.session_state.transcription_path
        and not st.session_state.transcribing
        and (
            # Check if we just uploaded or recorded
            "transcription_upload" in st.session_state
            or "audio_recorder" in st.session_state
        )
    ):
        st.session_state.transcribing = True
        st.rerun()


if __name__ == "__main__":
    transcription_page()
