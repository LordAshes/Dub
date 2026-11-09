# SRTCombine.py
import os
import sys
from pydub import AudioSegment
import pysrt

# CONFIG
SRT_FILE = sys.argv[1]
AUDIO_FOLDER = "results"
OUTPUT_FILE = "master.wav"

def load_audio(path):
    """Load audio and convert to PCM 16-bit mono."""
    audio = AudioSegment.from_file(path)
    return audio.set_channels(1).set_sample_width(2)

def format_ms(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:03d}"

def main():
    subs = pysrt.open(SRT_FILE)
    subs.sort(key=lambda x: x.start.ordinal)

    master_audio = AudioSegment.silent(duration=0)
    current_end_ms = 0

    for sub in subs:
        line_num = f"{sub.index:04d}"
        audio_path = os.path.join(AUDIO_FOLDER, f"Line_{line_num}.wav")

        if os.path.exists(audio_path):
            tts_audio = load_audio(audio_path)
            start_ms = sub.start.ordinal

            # Rubber-banding: start after previous audio if needed
            if start_ms > current_end_ms:
                # Add silence to reach the SRT start time
                master_audio += AudioSegment.silent(duration=start_ms - current_end_ms)

            # Append TTS audio
            master_audio += tts_audio

            # Update current_end_ms
            current_end_ms = len(master_audio)

            print(f"Added {audio_path} at {format_ms(current_end_ms - len(tts_audio))} (line {sub.index})")
        else:
            print(f"Skipping line {sub.index}, no audio found for {audio_path}")

    master_audio.export(OUTPUT_FILE, format="wav")
    print(f"Master audio exported to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
