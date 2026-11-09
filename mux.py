from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# === Configurable parameters ===
PRE_BUFFER_MS = 1000   # default: 1 second before
POST_BUFFER_MS = 1000  # default: 1 second after

# === Load audio files ===
original = AudioSegment.from_file("original_audio.wav")
tts = AudioSegment.from_file("master.wav")

# Ensure both tracks are aligned in frame rate / channels
if original.frame_rate != tts.frame_rate:
    original = original.set_frame_rate(tts.frame_rate)
if original.channels != tts.channels:
    original = original.set_channels(tts.channels)

# === Detect nonsilent regions in TTS ===
nonsilent_ranges = detect_nonsilent(
    tts, 
    min_silence_len=50,   # detects even very short pauses
    silence_thresh=-50    # dB threshold for "silence"
)

# === Apply pre/post buffers ===
buffered_ranges = []
for start, end in nonsilent_ranges:
    start = max(0, start - PRE_BUFFER_MS)
    end = min(len(tts), end + POST_BUFFER_MS)
    buffered_ranges.append((start, end))

# === Merge overlapping ranges ===
merged_ranges = []
for start, end in sorted(buffered_ranges):
    if not merged_ranges or start > merged_ranges[-1][1]:
        merged_ranges.append([start, end])
    else:
        merged_ranges[-1][1] = max(merged_ranges[-1][1], end)

# === Combine audio ===
combined = original[:]
for start, end in merged_ranges:
    combined = combined[:start] + tts[start:end] + combined[end:]

# === Export result ===
combined.export("combined_audio.wav", format="wav")
print("✅ Combined audio exported as combined_audio.wav")
