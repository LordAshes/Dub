@echo off
if exist *.srt del *.srt
if exist *.wav del *.wav
del /Q results\*.*
ffmpeg -i %1.%2 -map 0:m:language:eng %1.ENG.srt
rem ffmpeg -i %1.%2 -map 0:s:1 %1.ENG.srt
pause
ffmpeg -i %1.%2 -map 0:1 -c:a pcm_s16le original_audio.wav
python SRT2Audio.py %1.%2 %1.ENG.srt %1.ENG.srt
python SRTCombine.py %1.ENG.srt
python mux.py
ffmpeg -i %1.%2 -i combined_audio.wav -map 0:v:0 -map 0:a:0 -map 0:s? -map 1:a:0 -c:v copy -c:a:0 copy -c:a:1 aac -b:a:1 192k -c:s copy -metadata:s:a:1 title="English" -metadata:s:a:1 language=eng -shortest %1.ENG.%2