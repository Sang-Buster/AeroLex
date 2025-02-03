import librosa
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.audio_processing import calc_melspectrogram, calc_spectrum, moving_average

GRAPH_WIDTH = 1200
GRAPH_HEIGHT_2D = 500
GRAPH_HEIGHT_3D = 700
HOP = 1000


def plot_waveform(wav, sr):
    """Plot audio waveform"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=wav[::HOP], name="waveform"))

    fig.update_layout(
        title=dict(text="Sound Waveform", x=0.5, xanchor="center"),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT_2D,
        xaxis=dict(
            title="Time (s)",
            tickmode="array",
            tickvals=[0, len(wav[::HOP]) // 2, len(wav[::HOP])],
            ticktext=["0", str(int(len(wav) / (2 * sr))), str(int(len(wav) / sr))],
        ),
        yaxis=dict(title="Amplitude"),
    )
    return fig


def plot_spectrum(wav, sr, ave_win_len=100):
    """Plot frequency spectrum"""
    s_power, freqs = calc_spectrum(wav, sr)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=freqs, y=moving_average(s_power, ave_win_len), mode="lines")
    )

    fig.update_layout(
        title=dict(text="Frequency Spectrum", x=0.5, xanchor="center"),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT_2D,
        xaxis=dict(title="Frequency (Hz)"),
        yaxis=dict(title="Power"),
    )
    return fig


def plot_spectrogram(wav, sr, win_len=2048, hop_len=1024):
    """Plot regular spectrogram"""
    # Calculate spectrogram
    spec = librosa.stft(wav, n_fft=win_len, hop_length=hop_len)
    spec_db = librosa.amplitude_to_db(np.abs(spec), ref=np.max)

    # Create time and frequency arrays
    times = librosa.times_like(spec_db, sr=sr, hop_length=hop_len)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=win_len)

    # Create heatmap
    fig = px.imshow(
        spec_db,
        x=times,
        y=freqs,
        aspect="auto",
        origin="lower",
        labels=dict(x="Time (s)", y="Frequency (Hz)", color="dB"),
    )

    fig.update_layout(
        title=dict(text="Spectrogram", x=0.5, xanchor="center"),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT_2D,
        coloraxis_colorbar_title="dB",
    )

    return fig


def plot_melspectrogram(wav, sr, win_len=2048, hop_len=1024, n_mel=128):
    """Plot melspectrogram"""
    mel = calc_melspectrogram(wav, sr, win_len, hop_len, n_mel)
    mel_bins = librosa.mel_frequencies(n_mels=n_mel, fmin=0, fmax=int(sr / 2))

    fig = px.imshow(np.flipud(mel), aspect="auto", title="Melspectrogram")

    fig.update_layout(
        title=dict(text="Melspectrogram", x=0.5, xanchor="center"),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT_2D,
        xaxis=dict(title="Time"),
        yaxis=dict(
            title="Frequency (Hz)",
            tickmode="array",
            tickvals=[0, n_mel // 2, n_mel - 1],
            ticktext=[
                f"{int(mel_bins[0])}",
                f"{int(mel_bins[n_mel // 2])}",
                f"{int(mel_bins[-1])}",
            ],
        ),
    )
    return fig


def plot_3d_spectrogram(wav, sr, win_len=2048, hop_len=1024):
    """Plot 3D spectrogram showing volume, frequency and time"""
    # Calculate spectrogram
    spec = librosa.stft(wav, n_fft=win_len, hop_length=hop_len)
    spec_db = librosa.amplitude_to_db(np.abs(spec))

    # Create time and frequency arrays
    times = librosa.times_like(spec_db, sr=sr, hop_length=hop_len)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=win_len)

    # Create meshgrid for 3D plot
    time_grid, freq_grid = np.meshgrid(times, freqs)

    # Create 3D surface plot
    fig = go.Figure(
        data=[
            go.Surface(
                x=time_grid,
                y=freq_grid,
                z=spec_db,
                colorscale="Viridis",
                colorbar=dict(title="Volume (dB)"),
            )
        ]
    )

    fig.update_layout(
        title=dict(text="3D Spectrogram", x=0.5, xanchor="center"),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT_3D,
        scene=dict(
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            zaxis_title="Volume (dB)",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2), center=dict(x=0, y=0, z=-0.2)),
        ),
    )

    return fig
