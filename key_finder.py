import numpy as np
import librosa

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
KEYS = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']


def estimate_key(file_path: str) -> tuple[str, str]:
    """Estimate the musical key of an audio file and its relative key.
    A simple Krumhansl-Schmuckler-like algorithm is applied to the mean chroma
    vector of the audio. The function returns both the detected key and the
    relative ("alternate") key, which is the corresponding relative major or
    minor.
    """
    y, sr = librosa.load(file_path)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    major_scores = [np.corrcoef(np.roll(MAJOR_PROFILE, i), chroma_mean)[0, 1] for i in range(12)]
    minor_scores = [np.corrcoef(np.roll(MINOR_PROFILE, i), chroma_mean)[0, 1] for i in range(12)]

    best_major = np.argmax(major_scores)
    best_minor = np.argmax(minor_scores)

    if major_scores[best_major] >= minor_scores[best_minor]:
        key = f"{KEYS[best_major]} major"
        alt_idx = (best_major + 9) % 12  # relative minor
        alt_key = f"{KEYS[alt_idx]} minor"
    else:
        key = f"{KEYS[best_minor]} minor"
        alt_idx = (best_minor + 3) % 12  # relative major
        alt_key = f"{KEYS[alt_idx]} major"

    return key, alt_key
