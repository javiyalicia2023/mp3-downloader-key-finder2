import argparse
from i18n import set_language, t
from youtube_audio import download_audio
from key_finder import estimate_key
from audio_features import analyze_features, describe_score

def main():
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=["en", "es"], default="en")
    args, remaining = pre.parse_known_args()
    set_language(args.lang)

    parser = argparse.ArgumentParser(description=t("cli_description"), parents=[pre])
    parser.add_argument("url", help=t("arg_url"))
    parser.add_argument("--bitrate", type=int, choices=[160, 320], default=160,
                        help="Output MP3 bitrate in kbps (160 or 320)")
    parser.add_argument("--output-dir", default="downloads",
                        help=t("arg_output_dir"))
    parser.add_argument("--lang", choices=["en", "es"], default=args.lang,
                        help=t("arg_lang"))
    args = parser.parse_args(remaining)

    mp3_path = download_audio(args.url, bitrate=args.bitrate, output_dir=args.output_dir)
    print(t("audio_saved").format(mp3_path))
    
    key, alt_key = estimate_key(mp3_path)
    features = analyze_features(mp3_path)
    print(f"{t('detected_key')}: {key}")
    print(f"{t('relative_key')}: {alt_key}")
    print(f"{t('bpm')}: {features['bpm']:.2f}")
    print(f"{t('energy')}: {features['energy']:.2f} ({describe_score(features['energy'])})")
    print(f"{t('danceability')}: {features['danceability']:.2f} ({describe_score(features['danceability'])})")
    print(f"{t('happiness')}: {features['happiness']:.2f} ({describe_score(features['happiness'])})")

if __name__ == "__main__":
    main()
