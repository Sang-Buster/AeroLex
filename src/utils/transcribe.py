"""Real-time transcription utility using Whisper"""

import os
from datetime import datetime
from time import sleep

import numpy as np
import streamlit as st
import torch
import whisper
from pydub import AudioSegment


def check_for_stop_signal():
    """Check for stop signal file in the data directory"""
    stop_signal_path = os.path.join("src", "data", "text", "stop_signal.txt")
    return os.path.exists(stop_signal_path)


def send_stop_signal():
    """Create stop signal file in the data directory"""
    # Ensure directory exists
    os.makedirs(os.path.join("src", "data", "text"), exist_ok=True)
    stop_signal_path = os.path.join("src", "data", "text", "stop_signal.txt")
    with open(stop_signal_path, "w") as f:
        f.write("stop")


class WhisperTranscriber:
    def __init__(
        self,
        model_name: str,
        audio_path: str,
        energy_threshold=300,
        record_timeout=3.0,
        phrase_timeout=15.0,
        mic_index=0,
    ):
        """Initialize the transcriber with the specified model and audio path"""
        # Ensure model name is valid and doesn't have duplicate language suffix
        if model_name.endswith(".en.en"):
            model_name = model_name[:-3]  # Remove duplicate .en suffix

        self.model_name = model_name
        self.audio_path = audio_path
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.mic_index = mic_index

        # Set up output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Text output directory
        self.text_dir = os.path.join("src", "data", "text")
        os.makedirs(self.text_dir, exist_ok=True)
        self.transcription_path = os.path.join(
            self.text_dir, f"transcription_{timestamp}.txt"
        )
        self.summary_path = os.path.join(self.text_dir, f"summary_{timestamp}.json")

        # Load the model
        try:
            self.audio_model = whisper.load_model(self.model_name)
        except RuntimeError as e:
            available_models = whisper.available_models()
            st.error(
                f"Error loading model. Available models: {', '.join(available_models)}"
            )
            raise e

        self.transcription = [""]

    def process_audio_file(self):
        """Process a pre-recorded audio file"""
        # Load audio file
        audio = AudioSegment.from_file(self.audio_path)

        # Process in chunks
        chunk_duration = 30000  # 30 seconds
        total_duration = len(audio)
        current_transcription = []

        for start in range(0, total_duration, chunk_duration):
            if check_for_stop_signal():
                break

            end = min(start + chunk_duration, total_duration)
            chunk = audio[start:end]
            chunk_np = (
                np.array(chunk.get_array_of_samples()).astype(np.float32) / 32768.0
            )

            # Transcribe chunk
            result = self.audio_model.transcribe(
                chunk_np, fp16=torch.cuda.is_available()
            )
            text = result["text"].strip()

            # Update transcription
            current_transcription.append(text)
            full_transcription = "\n\n".join(current_transcription)

            # Write to transcription file
            with open(self.transcription_path, "w", encoding="utf-8") as file:
                file.write(full_transcription)

            yield full_transcription

            # Small delay to prevent overwhelming the UI
            sleep(0.1)

    def start(self):
        """Start the transcription process"""
        # Clear any existing transcription
        with open(self.transcription_path, "w", encoding="utf-8") as file:
            file.write("")

        if self.audio_path:
            yield from self.process_audio_file()
        else:
            raise ValueError("No audio source provided")

    def cleanup(self):
        """Clean up any temporary files"""
        stop_signal_path = os.path.join("src", "data", "text", "stop_signal.txt")
        if os.path.exists(stop_signal_path):
            os.remove(stop_signal_path)
