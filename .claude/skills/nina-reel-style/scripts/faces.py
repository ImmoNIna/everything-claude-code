"""Detect Nina's face per segment in raw.mp4 (OpenCV YuNet) -> faces.json."""
import json
import statistics

import cv2

det = cv2.FaceDetectorYN.create('yunet.onnx', '', (540, 960), 0.6, 0.3, 5000)
segs = json.load(open('segs.json'))
cap = cv2.VideoCapture('raw.mp4')
res = []
for i, s in enumerate(segs):
    found = []
    for f in (0.2, 0.5, 0.8):
        cap.set(cv2.CAP_PROP_POS_MSEC, (s['s'] + s['d'] * f) * 1000)
        ok, fr = cap.read()
        if not ok:
            continue
        _, fs = det.detect(cv2.resize(fr, (540, 960)))
        if fs is not None and len(fs):
            x, y, w, h = max(fs, key=lambda r: r[2] * r[3])[:4]
            found.append((float(x + w / 2) * 2, float(y + h / 2) * 2))
    res.append({'fx': statistics.median(a for a, _ in found),
                'fy': statistics.median(b for _, b in found)} if found else None)
    print(i, res[-1], flush=True)
last = next((r for r in res if r), {'fx': 540, 'fy': 700})
out = []
for r in res:
    last = r or last
    out.append(last)
json.dump(out, open('faces.json', 'w'))
print('END')
