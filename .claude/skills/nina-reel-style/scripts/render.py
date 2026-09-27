"""Cut raw.mp4 into face-centered 1080x1920 segments and join them -> joined.mkv."""
import json
import os
import subprocess

segs = json.load(open('segs.json'))
faces = json.load(open('faces.json'))
PHONE = "highpass=f=350,lowpass=f=3200,acompressor=threshold=-24dB:ratio=8:attack=5:release=60,volume=2.2,alimiter=limit=0.9,"
os.makedirs('segs', exist_ok=True)
with open('segs/list.txt', 'w') as lst:
    for i, s in enumerate(segs):
        out = f'segs/s{i:02d}.mkv'
        lst.write(f"file 's{i:02d}.mkv'\n")
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            continue
        fc = faces[i]
        # face centre lands at x=540, y=600; zoom only as much as needed (max 1.15)
        z = min(1.15, max(s['z'], 1320 / (1920 - fc['fy'])))
        W = int(round(1080 * z / 2) * 2)
        H = int(round(1920 * z / 2) * 2)
        cx = int(min(max(fc['fx'] * z - 540, 0), W - 1080))
        cy = int(min(max(fc['fy'] * z - 600, 0), H - 1920))
        vf = f"fps=30,scale={W}:{H}:flags=lanczos,crop=1080:1920:{cx}:{cy},format=yuv420p"
        d = s['d']
        af = f"afade=t=in:d=0.015,afade=t=out:st={d - 0.03:.3f}:d=0.03"
        if s['k'] == 'n':
            af = PHONE + af
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s['s']), '-i', 'raw.mp4', '-t', f'{d:.4f}',
                        '-vf', vf, '-af', af, '-ar', '48000', '-ac', '2', '-c:v', 'libx264', '-preset', 'veryfast',
                        '-crf', '17', '-threads', '1', '-c:a', 'pcm_s16le', out], check=True)
        print(i, flush=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'segs/list.txt', '-c', 'copy',
                'joined.mkv'], check=True)
print('JOINED', flush=True)
