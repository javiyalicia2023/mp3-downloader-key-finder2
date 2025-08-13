import argparse
from youtube_audio import download_audio
from key_finder import estimate_key
from audio_features import analyze_features, describe_score


def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio and estimate its key")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--bitrate", type=int, choices=[160, 320], default=160,
                        help="Output MP3 bitrate in kbps (160 or 320)")
    parser.add_argument("--output-dir", default="downloads",
                        help="Directory where the MP3 will be saved")
    args = parser.parse_args()

    mp3_path = download_audio(args.url, bitrate=args.bitrate, output_dir=args.output_dir)

    print(f"Audio saved to {mp3_path}")

    key, alt_key = estimate_key(mp3_path)
    features = analyze_features(mp3_path)

    print(f"Detected key: {key}")
    print(f"Relative key: {alt_key}")
    print(f"BPM: {features['bpm']:.2f}")
    print(f"Energy: {features['energy']:.2f} ({describe_score(features['energy'])})")
    print(f"Danceability: {features['danceability']:.2f} ({describe_score(features['danceability'])})")
    print(f"Happiness: {features['happiness']:.2f} ({describe_score(features['happiness'])})")


if __name__ == "__main__":
    main()
