import numpy as np
import librosa


def analyze_features(file_path: str) -> dict:
    """Calculate basic audio features for the given file.

    Returns a dictionary with BPM, energy, danceability and happiness scores.

    All feature scores are normalised to a 0-100 scale where higher values
    indicate a stronger presence of that quality.

    """
    y, sr = librosa.load(file_path)

    # BPM
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Energy as mean RMS
    rms = librosa.feature.rms(y=y)[0]
    energy = float(np.mean(rms) / np.max(rms) * 100) if np.max(rms) > 0 else 0.0

    # Danceability via onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    danceability = float(np.mean(onset_env) / np.max(onset_env) * 100) if np.max(onset_env) > 0 else 0.0

    # Happiness via spectral centroid
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    happiness = float(np.mean(centroid) / np.max(centroid) * 100) if np.max(centroid) > 0 else 0.0

    return {
        "bpm": float(tempo),
        "energy": energy,
        "danceability": danceability,
        "happiness": happiness,
    }



def describe_score(value: float) -> str:
    """Return a qualitative description for a 0-100 feature score."""
    if value < 33:
        return "low"
    if value < 66:
        return "medium"
    return "high"

