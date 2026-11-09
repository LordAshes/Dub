import os
import subprocess
import sys
import re

from pathlib import Path
from typing import List
from datetime import timedelta

MING_PATH = Path(__file__).parent / "ming-3.0-tts"
sys.path.insert(0, str(MING_PATH))

from ming_tts import MingTTS

SOURCE_INPUT_FILE = sys.argv[2]     # Original-language subtitles
AUDIO_FILE = sys.argv[1]            # Original movie/episode audio
FFMPEG_PATH = "ffmpeg"              # Assumes FFmpeg is in PATH

INPUT_FILE = sys.argv[3]
RESULTS_DIR = Path("./results")
RESULTS_DIR.mkdir(exist_ok=True)
OUTPUT_TEMPLATE = "Line_{:04d}.wav"

VOICE_SAMPLES_DIR = RESULTS_DIR / "voice_samples"
VOICE_SAMPLES_DIR.mkdir(exist_ok=True)

END_PUNCTUATION = () # Disables use of punctuation to end grouping. This will group multiple sentences together but can join to two speakers together if the gap is not set accurately.
# END_PUNCTUATION = (".", "!", "?") # Enabled use of punctuation to end grouping. This will break grouping by sentences which will provide shorter audio voice cloning samples.
MAX_GAP_SECONDS = 0.5  # Maximum gap between subtitles to consider them part of the same group

RESULTS_DIR.mkdir(exist_ok=True)

print(f"VIDEO SOURCE: {INPUT_FILE}")
print(f"ORIGNAL LANGUAGE SRT: {SOURCE_INPUT_FILE}")
print(f"TRANSLATED LANGUAGE SRT: {INPUT_FILE}")
print(f"RESULTS FOLDER: {RESULTS_DIR}")
print(f"VOICE SAMPLE FOLDER: {VOICE_SAMPLES_DIR}")

model = MingTTS("inclusionAI/Ming-3.0-tts-0.5b", text_normalization=False)

def parse_srt(file_path: str) -> List[dict]:
    entries = []
    with open(file_path, encoding='utf-8') as f:
        content = f.read().strip()
    blocks = re.split(r"\n\s*\n", content)
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) >= 3:
            index = int(lines[0])
            time_range = lines[1].replace(",", ".")
            start_str, end_str = re.split(r"\s*--?>\s*", time_range)
            start = srt_time_to_timedelta(start_str)
            end = srt_time_to_timedelta(end_str)
            text = " ".join(lines[2:]).strip()
            entries.append({"index": index, "start": start, "end": end, "text": text})
    return entries

def srt_time_to_timedelta(srt_time: str) -> timedelta:
    hours, minutes, seconds = srt_time.split(":")
    sec, millis = map(int, seconds.split("."))
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=sec, milliseconds=millis)

def group_entries(entries: List[dict]) -> List[List[dict]]:
    groups = []
    current_group = []

    for entry in entries:

        # Clean subtitle text while preserving the dictionary
        entry["text"] = clean_subtitle(entry["text"])

        if not current_group:
            current_group.append(entry)
            continue

        prev_entry = current_group[-1]
        time_gap = (entry["start"] - prev_entry["end"]).total_seconds()

        # Start a new group if the gap is too large
        if prev_entry["text"].strip().endswith(END_PUNCTUATION) or time_gap > MAX_GAP_SECONDS:
            groups.append(current_group)
            current_group = [entry]
        else:
            current_group.append(entry)

    if current_group:
        groups.append(current_group)

    return groups
    
def clean_subtitle(text: str) -> str:
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\{[^}]*}', '', text)
    return text.strip()

def generate_tts(group: List[dict], message: str,
                 source_entries: dict, output_path: Path):

    first_idx = group[0]["index"]
    last_idx = group[-1]["index"]

    # Determine the reference audio interval
    start_time = group[0]["start"].total_seconds()
    end_time = group[-1]["end"].total_seconds()
    duration = end_time - start_time

    if duration <= 0:
        raise ValueError(f"Invalid audio duration for group {first_idx}")

    # Create reference audio filename
    voice_sample_wav = VOICE_SAMPLES_DIR / f"Voice_{first_idx:04d}.wav"

    print(f"Creating Voice Sample: {voice_sample_wav}")

    # Extract original audio corresponding to the subtitle group
    command = [
        FFMPEG_PATH,
        "-y",
        "-ss", str(start_time),
        "-i", AUDIO_FILE,
        "-t", str(duration),
        "-vn",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        "-loglevel", "quiet",
        str(voice_sample_wav)
    ]

    subprocess.run(command, check=True)

    # # Retrieve original-language subtitle text
    # source_text = " ".join(
    #     source_entries[e["index"]]["text"]
    #     for e in group
    # )

    print(f"Creating TTS: {output_path}")

    # Generate translated speech using the cloned voice
    model.synthesize(
        task="TTS",
        language_id="English",
        text=message,
        prompt_wav_path=str(voice_sample_wav),
        # prompt_text=source_text,
        use_spk_emb=True,
        output_path=str(output_path),
    )
    
def has_text(text: str) -> bool:
    return any(char.isalpha() for char in text)
    
def process_srt():
    # Load translated subtitles
    entries = parse_srt(INPUT_FILE)

    # Load original-language subtitles
    original_entries = parse_srt(SOURCE_INPUT_FILE)

    # Create lookup dictionary using subtitle indices
    source_entries = {
        entry["index"]: entry
        for entry in original_entries
    }

    # Group translated subtitles
    groups = group_entries(entries)

    for group in groups:
        first_idx = group[0]["index"]
        last_idx = group[-1]["index"]

        # Combine translated text
        combined_text = " ".join(e["text"] for e in group)

        # Verify that corresponding original subtitles exist
        missing = [
            e["index"] for e in group
            if e["index"] not in source_entries
        ]

        if missing:
            raise ValueError(
                f"Missing original subtitle entries: {missing}"
            )

        preview = combined_text[:40] + (
            "..." if len(combined_text) > 40 else ""
        )

        range_label = (
            f"[{first_idx}-{last_idx}]"
            if first_idx != last_idx
            else f"[{first_idx}]"
        )

        print(f"{range_label} {preview}")

        output_file = RESULTS_DIR / OUTPUT_TEMPLATE.format(first_idx)

        if has_text(combined_text):
            generate_tts(
                group,
                combined_text,
                source_entries,
                output_file
            )
        
if __name__ == "__main__":
    process_srt()
