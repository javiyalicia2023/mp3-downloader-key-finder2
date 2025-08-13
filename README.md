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

## Graphical interface

For a simple GUI with a black/#2F5BF9/white palette, run:

```
python gui.py
```

The interface lets you choose a download directory, enter a YouTube URL and
bitrate, or import/drag audio files for analysis. Results show the detected
key, relative key, BPM, energy, danceability and happiness.




### Requirements

Install dependencies with:

```
pip install -r requirements.txt
```

`yt-dlp` relies on `ffmpeg` for conversion to MP3. Ensure `ffmpeg` is available
on your system.


## Audio metrics

The analysis module reports three additional scores on a 0-100 scale:

- **Energy** – approximates the loudness and intensity of the track using RMS
  energy. Values near 0 indicate calm or quiet audio, while values near 100
  represent very energetic material.
- **Danceability** – derived from onset strength and hints at how suitable a
  track is for dancing. Higher numbers suggest a more pronounced and stable
  beat.
- **Happiness** – uses spectral centroid as a proxy for brightness; lower scores
  correspond to darker or sadder timbres, whereas higher scores imply brighter,
  more cheerful sounds.

Interpretation guide: 0–33 → low, 34–66 → medium, 67–100 → high.

