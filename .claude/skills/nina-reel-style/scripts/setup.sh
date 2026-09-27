#!/usr/bin/env bash
# One-time setup in the Composio sandbox (1 CPU, 1 GB RAM): font + face model.
set -e
mkdir -p ~/.fonts
[ -f ~/.fonts/Montserrat.ttf ] || curl -sSL -o ~/.fonts/Montserrat.ttf \
  "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
[ -f ~/.fonts/Fredoka.ttf ] || curl -sSL -o ~/.fonts/Fredoka.ttf \
  "https://github.com/google/fonts/raw/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf"
fc-cache -f >/dev/null
[ -f yunet.onnx ] || curl -sSL -o yunet.onnx \
  https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
echo SETUP_OK
