#!/usr/bin/env bash
# Burn captions/table, speed 1.1, hook overlay (hook.png, first 3.2 s), loudness -14 LUFS -> final.mp4
# Split passes to stay under 1 GB RAM.
set -e
ffmpeg -v error -y -i joined.mkv -vn -af atempo=1.1,loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 aud.m4a
echo AUD
python3 hook.py
ffmpeg -v error -y -i joined.mkv -loop 1 -t 3.2 -framerate 30 -i hook.png -an -filter_complex \
  "[0:v]ass=subs.ass,setpts=PTS/1.1,fps=30[v];[1:v]format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st=3.05:d=0.15:alpha=1[h];[v][h]overlay=0:0:eof_action=pass,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 19 -x264-params rc-lookahead=10:ref=2:threads=1 vid.mp4
echo VID
ffmpeg -v error -y -i vid.mp4 -i aud.m4a -map 0:v -map 1:a -c copy -shortest -movflags +faststart final.mp4
echo DONE
