"""Cut raw.mp4 into face-centred 1080x1920 segments and join them -> joined.mkv.

Framing rules (Nina):
- face centre at x=540, y=FACE_Y (high, so captions never cover the mouth)
- during the hook (first ~3.3 s of output) the face stays low (no upward shift),
  so the hook box sits above her head like in her feed
- about every 5-7 s one segment gets a smooth zoom in or out (alternating)
"""
import json
import os
import subprocess

FACE_Y = 520
HOOK_END = 3.3
ZMAX = 1.3
MOVE_EVERY = 5.5  # seconds of output between smooth zooms
MOVE_AMOUNT = 0.10

segs = json.load(open('segs.json'))
faces = json.load(open('faces.json'))
PHONE = ("highpass=f=350,lowpass=f=3200,acompressor=threshold=-24dB:ratio=8:attack=5:release=60,"
         "volume=2.2,alimiter=limit=0.9,")
os.makedirs('segs', exist_ok=True)
t_out, since_move, move_dir = 0.0, 0.0, 1
with open('segs/list.txt', 'w') as lst:
    for i, s in enumerate(segs):
        out = f'segs/s{i:02d}.mkv'
        lst.write(f"file 's{i:02d}.mkv'\n")
        d = s['d']
        fx, fy = faces[i]['fx'], faces[i]['fy']
        in_hook = t_out < HOOK_END
        ty = fy if in_hook else FACE_Y
        z = s['z'] if in_hook else min(ZMAX, max(s['z'], (1920 - ty) / max(1, 1920 - fy)))
        move = (not in_hook) and since_move >= MOVE_EVERY and d >= 1.5 and s['k'] == 't'
        t_out += d
        since_move = 0.0 if move else since_move + d
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            if move:
                move_dir *= -1
            continue
        if move:
            z0, z1 = (z, z + MOVE_AMOUNT) if move_dir > 0 else (z + MOVE_AMOUNT, z)
            move_dir *= -1
            n = max(1, int(round(d * 30)))
            # zoompan on a 2x upscale for smooth sub-pixel motion
            vf = (f"fps=30,scale=2160:3840:flags=bicubic,"
                  f"zoompan=z='{z0}+({z1 - z0})*on/{n}':"
                  f"x='max(0,min(iw-iw/zoom,{2 * fx}-1080/zoom))':"
                  f"y='max(0,min(ih-ih/zoom,{2 * fy}-{2 * ty}/zoom))':d=1:s=1080x1920:fps=30,format=yuv420p")
        else:
            W = int(round(1080 * z / 2) * 2)
            H = int(round(1920 * z / 2) * 2)
            cx = int(min(max(fx * z - 540, 0), W - 1080))
            cy = int(min(max(fy * z - ty, 0), H - 1920))
            vf = f"fps=30,scale={W}:{H}:flags=lanczos,crop=1080:1920:{cx}:{cy},format=yuv420p"
        af = f"afade=t=in:d=0.015,afade=t=out:st={d - 0.03:.3f}:d=0.03"
        if s['k'] == 'n':
            af = PHONE + af
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s['s']), '-i', 'raw.mp4', '-t', f'{d:.4f}',
                        '-vf', vf, '-af', af, '-ar', '48000', '-ac', '2', '-c:v', 'libx264', '-preset', 'veryfast',
                        '-crf', '17', '-threads', '1', '-c:a', 'pcm_s16le', out], check=True)
        print(i, 'move' if move else '', flush=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'segs/list.txt', '-c', 'copy',
                'joined.mkv'], check=True)
print('JOINED', flush=True)
