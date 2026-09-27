#!/usr/bin/env bash
# Burn captions/table, speed 1.1, loudness -14 LUFS -> final.mp4 (split passes to stay under 1 GB RAM)
set -e
ffmpeg -v error -y -i joined.mkv -vn -af atempo=1.1,loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 aud.m4a
echo AUD
ffmpeg -v error -y -i joined.mkv -an -vf ass=subs.ass,setpts=PTS/1.1,fps=30 -c:v libx264 -preset veryfast -crf 19 \
  -x264-params rc-lookahead=10:ref=2:threads=1 -pix_fmt yuv420p vid.mp4
echo VID
ffmpeg -v error -y -i vid.mp4 -i aud.m4a -map 0:v -map 1:a -c copy -shortest -movflags +faststart final.mp4
echo DONE
