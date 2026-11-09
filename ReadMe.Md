# DUB 1.0

This projects takes a foreign language video which contains English subtitles. It extracts the subtitles and generates a English soundstrack based on the extracted SRT subtiles and the original voice samples.

## Prerequisites

The Dub project requires access to FFMPEG. You need to have FFMPEG installed and added to your PATH so that the Dub project can call this tool to extract subtitles, audio and rebuild the translated audio.

The installtion of this tool is beyond the scope of this document.

## Installation (One Time)

Clone the repo with:

```
git clone https://github.com/LordAshes/Dub.git
cd Dub
```

Make and activate a Python 3.12 based environment using:

```
py -3.12 -m venev env
.\env\Scripts\activate
```

Download the flash-attn wheel for installing flash-attn on Windows from:

```
https://huggingface.co/lldacing/flash-attention-windows-wheel/tree/main
```

Download the file:

```
flash_attn-2.7.4+cu124torch2.6.0cxx11abiFALSE-cp312-cp312-win_amd64.whl
```

Install the repo requirements using:

```
pip install -r requirements.txt
```

Download the Ming-3.0-TTS model using:

```
hf download inclusionAI/Ming-3.0-tts-0.5b --local-dir Ming-3.0-tts-0.5b
```

## Usage

To use the Dub project, switch to the Dub repo folder and activate the environment:

```
.\env\Scripts\activate
```

Copy the video file to the Dub folder. Ensure that the video file has embedded English subtitles.
The Dub project can be used with external subtiles but the easy to use BAT file assumes that the
video files contains an English subtile track (among possible other subtile tracks).

Start the Dub process by providing the video file name and extension as separate parameters to
the Dub.Bat file. Not that the name and extension are separated by a space not a period.

```
Dub MyVideo MyVideoExtension
```

Example:

```
Dub MacGuyver Mkv
```

This will execute the entire Dub process generating a new video file with the same name as the
original but with ``.ENG`` appended to the end before the extension. The newly created video file
contains both the original soundtrack (default soundtrack) and the TTS dub soundtrack.

## Components

The Dub process BAT file executes a number of steps to complete the Dub process. If, for some reason,
the DUB BAT file cannot be used (e.g. the original video does not have English subtitles and you
want to use an external subtitle SRT file), it may still be possible to complete the dub process
by executing the steps manually.

The DUB BAT file processes the following steps in the order listed...

### Subtile Extraction

The BAT files use the following to extract the subtitles:

```
ffmpeg -i %1.%2 -map 0:m:language:eng %1.ENG.srt
```

If video file contains English subtitles but they are not marked as such, you may be able to
extract the subtitle by track instead of name using:

```
rem ffmpeg -i %1.%2 -map 0:s:# %1.ENG.srt
```

Where ``#`` is a number, such as 1, that corresponds to the subtitle track to extract.
The first subtitle track typically starts at 0.

### Original Audio Extraction

Next the original audio soundtrack is extracted under the name ``original_audio.wav``.
The format of the wav file is ``PCM S16LE``.

### TTS Creation (via SRT2Audio.py)

The SRT2Audio.py script is responsible for grouping subtitles, extracting voice samples,
and generating the translated TTS based on the provided SRT subtitles file.

The syntax for the SRT2Audio.py is:

``python SRT2Audio.py video_file foreign_SRT_file English_SRT_file``

However, currently the use of the ``foreign_SRT_file`` is not fully implemented, so use:

``python SRT2Audio.py video_file English_SRT_file English_SRT_file``

For example:

``python SRT2Audio.py MacGuyver.mkv MacGuyver.Eng.Srt MacGuyver.Eng.Srt``

The result of this script is a bunch of WAV files, corresponding to each subtitles grouping, in the ``results`` folder.
In addition, the voice smaples, used for each subtitles grouping, are contained in a subfolder off of the ``results`` folder.

Subtitle groupings are done by a time gap. When the time gap between subtitles exceeds the configured threshold gap,
the script treats the following subtitles as a new grouping. This is not a perfect solution to determining when
subtitles correspond to a different character but with a properly set gap threshold it is correct most of the time.
The solution breaks down when two or more different characters speak, one after each other, without a pause in between.
In such cases, the solution merges both characters speaking and will generate TTS based on both their voices.
This is the solution's trade off against having to implement much more complex algorithms for detecting the speaking
character.

The gap threshold can be configured by opening up the SRT2Audio.py and finding the line:

```
MAX_GAP_SECONDS = 0.5  # Maximum gap between subtitles to consider them part of the same group

``` 

Setting this value lower means that subtitles will be broken into smaller sections and each of those sections will
resample the voice that is speaking them. This will lead to a more accurate detection of who is speaking but it can
lead to the segments being too small to properly sample the voice and/or sentences being broken up and thus generating
odd intonation.

Setting the value higher means that more subtitles will be groups together but it also means that if two or more
different characters speak quickly after each other, their content will get grouped together and thus spoken by the
same voice.

### TTS Creation (via SRTCombine.py)

The SRTCombine.py script combines the individual WAV files generated by the SRT2Audio.py script into a single WAV
file that preserves the position of each WAV file in the original soundtrack.

The syntax for the SRTCombine.py is:

```
python SRTCombine.py video_file_name.ENG.srt
```

For example:

```
python SRTCombine.py MacGuyver.ENG.srt
```

The script expect the indivisual WAV files in the ``results`` folder and write out the single TTS file as ``master.wav``.

The ``master.wav`` has all of the translated TTS content, at the correct audio position, but it does not contain any
of the original soundtrack audio.

### Combine TTS with Original Soundtrack (via mux.py)

The mux.py script combines the ``master.wav`` file created by the SRTCombine.py script with the original soundtrack
in places where characters are not speaking. This generates a audio file which matches the original soundtrack except
the foreign speaking is replaced with TTS translated speech.

The mux.py string does not take any parameters. Its expected inputs are hard coded.

```
python mux.py
```

The mux.py script expects ``original_audio.wav`` and ``master.wav`` in the same folder as the script.
The ``original_audio.wav`` file was extrascted earlier by a FFMPEG command.
The ``master.wav`` file was generated by the SRTCombine.py script above.

### Insertion of the Translated Audio Track

Lastly the muxed audio file containing the original audio expect for speech replaced by translated TTS, is inserted
into the original video as an additional audio soundtrack. This process does not remove the original soundtrack,
so that the video can be watched in the original languages with subtitles. Instead it adds the audio track as an
additional track allowing the user to choose which way they want to enjoy the content.

The corresponding FFMPEG command is:

```
ffmpeg -i %1.%2 -i combined_audio.wav -map 0:v:0 -map 0:a:0 -map 0:s? -map 1:a:0 -c:v copy -c:a:0 copy -c:a:1 aac -b:a:1 192k -c:s copy -metadata:s:a:1 title="English" -metadata:s:a:1 language=eng -shortest video_file_name.ENG.video_file_extension
```

For example:

```
ffmpeg -i %1.%2 -i combined_audio.wav -map 0:v:0 -map 0:a:0 -map 0:s? -map 1:a:0 -c:v copy -c:a:0 copy -c:a:1 aac -b:a:1 192k -c:s copy -metadata:s:a:1 title="English" -metadata:s:a:1 language=eng -shortest MacGuyver.ENG.Mkv
```

## Limitations

1. As noted above, the solution uses a gap threshold to identify when speech may have switched from one character to another. This is a reasonable approximation which should detect character switch in most situation, especially if the user plays around with the gap threshold. However, it is not perfect. Any time there is quick succesive dialog by multiple charcters there is a chance that the solution will group the speech together and reproduce it using a single voice. 

2. If the gap threshold is set low then the speech may be divided into small segments which may not be long enough for the system to be able to get a good voice smaple. This may cause voice to sound less like its original.

3. Any subtiles added which are not actually said (e.g. episode number and name, disclaimers, etc) will use the default Ming-3.0-tts voice.

These limitations are a trade off against more complicated character speaking detection algorithms. The current solution does not need to understand who is speaking because it just samples the original audio to determine what voice it should use for the corresponding transaltion. As such it does not need SRT clues as to who is speaking or the corresponding video to determine who is speaking. While such advanced analytics are possible and would yield a more accurate solution, they would make the solution a lot more complicated and take a lot longer to process. This solution is intended as a less accurate alternative which in many cases may be good enough.

## Credit

The Ming-3.0-tts folder is a clone of the Ming-3.0-tts repo created by ``InclusionAI``. It is included in this repo for convenience. If you prefer to clone the repo yourself, you can do so with:

```
git clone https://github.com/inclusionAI/Ming-3.0-tts.git
```
















