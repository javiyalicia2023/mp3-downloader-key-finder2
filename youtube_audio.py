import os
import subprocess
from typing import Optional

def download_audio(url: str, bitrate: int = 160, output_dir: str = "downloads") -> str:
    """Download a YouTube video's audio as an MP3 file.

    Parameters
    ----------
    url: str
        The YouTube URL to download.
    bitrate: int, optional
        MP3 bitrate in kbps. Supported values: 160 or 320.
    output_dir: str, optional
        Directory where the resulting MP3 will be saved.

    Returns
    -------
    str
        Path to the downloaded MP3 file.
    """
    if bitrate not in (160, 320):
        raise ValueError("bitrate must be 160 or 320 kbps")

    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "-x",  # extract audio
        "--audio-format",
        "mp3",
        "--audio-quality",
        f"{bitrate}k",
        "-o",
        output_template,
        url,
    ]

    subprocess.run(cmd, check=True)

    # After downloading, find the most recent file in the directory
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir)]
    files = [f for f in files if f.endswith(".mp3")]
    if not files:
        raise FileNotFoundError("No MP3 file was created")
    latest_file = max(files, key=os.path.getctime)
    return latest_file
