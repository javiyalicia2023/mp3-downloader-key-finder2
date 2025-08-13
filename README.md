# mp3-downloader-key-finder

This command-line tool downloads a YouTube video, extracts the audio as an MP3
file (160 kbps or 320 kbps), and then analyzes several musical features of the
track. It reports the detected key along with its relative (alternate) key and
basic audio metrics such as BPM, energy, danceability and happiness.

## Usage

```
python main.py <youtube_url> [--bitrate 160|320]
```

The downloaded file is stored in the `downloads/` directory and the analyzed
features are printed to the console.

### Requirements

Install dependencies with:

```
pip install -r requirements.txt
```

`yt-dlp` relies on `ffmpeg` for conversion to MP3. Ensure `ffmpeg` is available
on your system.
