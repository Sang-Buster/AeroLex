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


def load_and_process_audio(file_path):
    """Load and process audio file"""
    wav, sr = librosa.load(file_path, sr=None)
    return wav, sr
