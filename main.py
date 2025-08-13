import argparse
from youtube_audio import download_audio
from key_finder import estimate_key

def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio and estimate its key")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--bitrate", type=int, choices=[160, 320], default=160,
                        help="Output MP3 bitrate in kbps (160 or 320)")
    args = parser.parse_args()

    mp3_path = download_audio(args.url, bitrate=args.bitrate)
    print(f"Audio saved to {mp3_path}")

    key = estimate_key(mp3_path)
    print(f"Detected key: {key}")

if __name__ == "__main__":
    main()
