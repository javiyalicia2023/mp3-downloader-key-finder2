# mp3-downloader-key-finder

This simple command-line tool downloads a YouTube video, extracts the audio as
an MP3 file (160 kbps or 320 kbps), and then estimates the musical key of the
track.

## Usage

```
python main.py <youtube_url> [--bitrate 160|320]
```

The downloaded file is stored in the `downloads/` directory and its detected key
is printed to the console.

### Requirements

Install dependencies with:

```
pip install -r requirements.txt
```

`yt-dlp` relies on `ffmpeg` for conversion to MP3. Ensure `ffmpeg` is available
on your system.
