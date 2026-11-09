import os
import re
import shutil
import tempfile
from pathlib import Path
from pydub import AudioSegment

# Configuration
INPUT_FILE = "input.txt"
PIPER_PATH = Path("piper.exe")
MODEL_PATH = Path("./models/en_US-hfc_female-medium.onnx")
CONFIG_PATH = Path("./models/en_US-hfc_female-medium.onnx.json")
OUTPUT_FILE = Path("master.wav")
TEMP_DIR = Path(tempfile.mkdtemp())
USE_CUDA = True  # Set False to disable CUDA

# Audio configuration
SAMPLE_RATE = 22050  # Match Piper output
CHANNELS = 1

END_PUNCTUATION = (".", "!", "?")

def run_piper(text: str, output_path: Path):
    temp_text_path = TEMP_DIR / "snippet.txt"
    with open(temp_text_path, "w", encoding="utf-8") as f:
        f.write(text)

    cmd = f'type "{temp_text_path}" | "{PIPER_PATH}" {"--cuda" if USE_CUDA else ""} --model "{MODEL_PATH}" --config "{CONFIG_PATH}" --output_file "{output_path}"'
    os.system(cmd)

def split_text_and_delays(content: str):
    segments = []
    buffer = ""
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("~"):
            if buffer:
                segments.extend(split_into_sentences(buffer))
                buffer = ""
            delay = int(re.findall(r"\d+", line)[0])
            segments.append({"type": "delay", "value": delay})
        else:
            buffer += " " + line
    if buffer:
        segments.extend(split_into_sentences(buffer))
    return segments

def split_into_sentences(text):
    sentence_end = re.compile(r"(?<=[.!?]) +")
    sentences = sentence_end.split(text.strip())
    return [{"type": "text", "value": s.strip()} for s in sentences if s.strip()]

def combine_audio_clips(clips: list, output_path: Path):
    master = AudioSegment.silent(duration=0)
    for clip in clips:
        master += clip
    master.export(output_path, format="wav")

def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        content = f.read()

    segments = split_text_and_delays(content)
    combined_clips = []
    for idx, segment in enumerate(segments):
        if segment["type"] == "delay":
            print(f"Inserting delay: {segment['value']} ms")
            combined_clips.append(AudioSegment.silent(duration=segment["value"]))
        else:
            print(f"Synthesizing: \"{segment['value'][:40]}\"")
            output_path = TEMP_DIR / f"clip_{idx:04d}.wav"
            run_piper(segment["value"], output_path)
            clip = AudioSegment.from_wav(output_path)
            combined_clips.append(clip)

    print(f"Combining {len(combined_clips)} audio segments...")
    combine_audio_clips(combined_clips, OUTPUT_FILE)

    print(f"Output saved to {OUTPUT_FILE}")
    shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    main()
