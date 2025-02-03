"""Audio processing utilities"""

import os
from datetime import datetime

import librosa
import librosa.display
import numpy as np


def calc_melspectrogram(wav, sr, win_len=2048, hop_len=1024, n_mel=128):
    """Calculate melspectrogram from audio data"""
    mel = librosa.feature.melspectrogram(
        y=wav,
        sr=sr,
        n_fft=win_len,
        hop_length=hop_len,
        win_length=win_len,
        n_mels=n_mel,
    )
    mel = librosa.power_to_db(mel, ref=np.max)
    return mel


def calc_spectrum(wav, sr):
    """Calculate frequency spectrum"""
    spectrum = np.abs(np.fft.fft(wav, sr)[: int(sr / 2)])
    freqs = np.fft.fftfreq(sr, d=1.0 / sr)[: int(sr / 2)]
    s_power = np.abs(spectrum)
    return s_power, freqs


def moving_average(ts, window):
    """Calculate moving average of time series data"""
    ts_pad = np.pad(ts, [int(window / 2), int(window / 2)], "reflect")
    return np.convolve(ts_pad, np.full(window, 1 / window), mode="same")[
        int(window / 2) : -int(window / 2)
    ]


def save_audio_file(audio_file):
    """Save uploaded audio file"""
    # Create a timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.wav"
    save_path = os.path.join("src/data/audio", filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Handle both uploaded files and recorded audio
    if hasattr(audio_file, "getvalue"):  # File uploader
        with open(save_path, "wb") as f:
            f.write(audio_file.getbuffer())
    else:  # Audio recorder
        with open(save_path, "wb") as f:
            f.write(audio_file.tobytes())

    return save_path


def load_and_process_audio(file_path):
    """Load and process audio file"""
    # Load audio file
    wav, sr = librosa.load(file_path, sr=None)
    return wav, sr
