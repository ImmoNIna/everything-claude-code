"""Build segs.json + subs.ass for a Nina ranking reel.

Input: project.json with keys
  words: [[start_ms, end_ms, "word"], ...]   (word timings from the transcript)
  plan:  [["t"|"n"|"p", start_s, end_s], ...] t=talk, n=street name, p="Platz X"
  fix:   {"wrong": "right", ...}             caption spelling fixes
  hook:  "Hook line 1\\NHook line 2"
  places: number of rows in the ranking table
Output: segs.json (cut list for render.py), subs.ass (captions, hook, table)
"""
import json

P = json.load(open('project.json'))
words = [(a / 1000, b / 1000, t) for a, b, t in P['words'] if '__silence' not in t]
FIX = P.get('fix', {})
PLAN = P['plan']
HOOK = P['hook']
NPL = P.get('places', 6)
R0 = P.get('first_rank', 1)  # e.g. 6 for 'Teil 2 (Platz 10 bis 6)'
FPS = 30

segs, subs, t_out, zi = [], [], 0.0, 0
for kind, a, b in PLAN:
    base = 1.15 if kind in 'np' else (1.0 if zi % 2 == 0 else 1.08)
    if kind == 't':
        zi += 1
    ws = [w for w in words if a - 0.01 <= w[0] <= b + 0.01]
    groups = [[ws[0]]]
    for w in ws[1:]:
        if w[0] - groups[-1][-1][1] > 0.28:
            groups.append([w])
        else:
            groups[-1].append(w)
    for g in groups:
        s = max(0, g[0][0] - 0.07)
        e = g[-1][1] + 0.12
        dur = round((e - s) * FPS) / FPS
        segs.append({'s': round(s, 3), 'd': round(dur, 4), 'k': kind, 'z': base})
        for w in g:
            subs.append((t_out + (w[0] - s), t_out + (w[1] - s), FIX.get(w[2], w[2]), kind))
        t_out += dur
json.dump(segs, open('segs.json', 'w'))
print('segments', len(segs), 'duration', round(t_out, 1))


def ts(x):
    x = max(0, x)
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


YEL = r'{\c&H00E6FF&}'
WHT = r'{\c&HFFFFFF&}'
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,2,2,60,60,870,1
Style: Name,Montserrat,96,&H0000E6FF,&H0000E6FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,9,3,2,50,50,870,1
Style: Tbl,Montserrat,48,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,0,0,0,1
Style: Title,Montserrat,56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,1,5,0,0,0,1
Style: TitleBox,Montserrat,72,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,24,0,5,0,0,0,1
Style: Hook,Montserrat,66,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,22,0,8,90,90,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = [f"Dialogue: 2,{ts(0)},{ts(3.2)},Hook,,0,0,0,,{{\\fad(120,150)}}{HOOK}"]

# caption groups: max 3 words, break after punctuation; names and "Platz X" kept whole
groups = []
for w in subs:
    if groups:
        g = groups[-1]
        last = g[-1]
        if last[3] == w[3] and w[3] in 'np' and w[0] - last[1] < 0.5:
            g.append(w)
            continue
        if (len(g) < 3 and last[3] == w[3] and w[3] not in 'np'
                and not last[2].endswith(('.', '?', '!', ',', ':')) and w[0] - last[1] < 0.5):
            g.append(w)
            continue
    groups.append([w])

for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0][0] if gi + 1 < len(groups) else 1e9
    kind = g[0][3]
    if kind == 'n':
        continue  # street names are shown by the title box instead
    if kind == 'p':
        txt = ' '.join(x[2] for x in g).upper().rstrip('.')
        ev.append(f"Dialogue: 1,{ts(g[0][0])},{ts(min(g[-1][1] + 0.12, nxt))},Name,,0,0,0,,"
                  f"{{\\fscx115\\fscy115\\t(0,120,\\fscx100\\fscy100)}}{txt}")
        continue
    end = min(g[-1][1] + 0.15, nxt)
    for k, w in enumerate(g):
        st = w[0] if k else g[0][0]
        en = g[k + 1][0] if k + 1 < len(g) else end
        parts = [(YEL if j == k else WHT) + x[2] for j, x in enumerate(g)]
        pop = r'{\fscx108\fscy108\t(0,90,\fscx100\fscy100)}' if k == 0 else ''
        ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{pop}" + ' '.join(parts))

# ---- ranking table ----
places, cur = [], None
for g in groups:
    k = g[0][3]
    if k == 'n':
        cur = {'name': ' '.join(x[2] for x in g).rstrip('.').replace('- ', '-'), 'ns': g[0][0]}
    elif k == 'p' and cur:
        cur['rank'] = int(''.join(c for c in g[-1][2] if c.isdigit()))
        cur['ps'] = g[0][0]
        places.append(cur)
        cur = None
END = t_out + 1
W, RH, GAP, NB = 600, 78, 8, 80
X0 = (1080 - W) // 2
Y0 = 1680 - (NPL * RH + (NPL - 1) * GAP)
# default: Platz 1 green (top) ... last place red; project "order": "red_top" flips it
PAL = ['22B55A', '8BCB4A', 'F4C63D', 'F08A3E', 'EE5A28', 'B71C1C']
if P.get('order') == 'red_top':
    PAL = PAL[::-1]
COL = {r: PAL[round((r - 1) * (len(PAL) - 1) / max(1, NPL - 1))] for r in range(1, NPL + 1)}  # r = table row


def bgr(h, f=1.0):
    r, g, b = [int(int(h[i:i + 2], 16) * f) for i in (0, 2, 4)]
    return f'&H{b:02X}{g:02X}{r:02X}&'


def rr(w, h, r=12):
    return (f"m {r} 0 l {w-r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h-r} b {w} {h} {w} {h} {w-r} {h} "
            f"l {r} {h} b 0 {h} 0 {h} 0 {h-r} l 0 {r} b 0 0 0 0 {r} 0")


for rk in range(1, NPL + 1):
    y = Y0 + (rk - 1) * (RH + GAP)
    ev.append(f"Dialogue: 3,{ts(0)},{ts(END)},Tbl,,0,0,0,,{{\\an7\\pos({X0},{y})\\bord0\\shad0\\1c{bgr(COL[rk])}\\1a&H10&\\p1}}{rr(W, RH)}{{\\p0}}")
    ev.append(f"Dialogue: 4,{ts(0)},{ts(END)},Tbl,,0,0,0,,{{\\an7\\pos({X0},{y})\\bord0\\shad0\\1c{bgr(COL[rk], 0.78)}\\p1}}{rr(NB, RH)}{{\\p0}}")
    ev.append(f"Dialogue: 5,{ts(0)},{ts(END)},Tbl,,0,0,0,,{{\\an5\\pos({X0 + NB // 2},{y + RH // 2})\\fs56}}{rk + R0 - 1}")

TX, TY = 540, 1112
for p in places:
    y = Y0 + (p['rank'] - R0) * (RH + GAP) + RH // 2
    bx = X0 + NB + (W - NB) // 2
    a, s = p['ns'], p['ps']
    name = p['name']
    est = len(name) * 0.42
    fb = int(min(56, (W - NB - 30) / (est * 0.85)))
    bs = int(min(100, 100 * (W - NB - 30) / (est * fb)))
    ev.append(f"Dialogue: 6,{ts(a)},{ts(s)},TitleBox,,0,0,0,,{{\\an5\\q2\\pos({TX},{TY})\\fscx115\\fscy115\\t(0,160,\\fscx100\\fscy100)}}{name}")
    ev.append(f"Dialogue: 6,{ts(s)},{ts(END)},Title,,0,0,0,,{{\\an5\\q2\\fs{fb}\\move({TX},{TY},{bx},{y},0,550)"
              f"\\fscx{int(7200 / fb)}\\fscy{int(7200 / fb)}\\t(0,550,\\fscx{bs}\\fscy100)}}{name}")
print('places', [(p['rank'], p['name']) for p in places])
open('subs.ass', 'w').write(hdr + '\n'.join(ev) + '\n')
