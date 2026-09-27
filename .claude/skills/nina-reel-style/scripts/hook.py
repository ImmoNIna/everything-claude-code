"""Render the hook title (first 3.2 s) as hook.png, exactly like Nina's feed reels.

One white box with slightly rounded corners, black Montserrat Bold 68 px,
normal upper/lower case, centred lines. Box 808 px wide, top at y=360
(below the Instagram top UI). Text from project.json "hook"; "\\N" forces a
line break, long lines wrap automatically. Never move it higher or make it smaller.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.expanduser('~/.fonts/Montserrat.ttf')
TOP, BOX_W, SIZE, PADY, LINE, RADIUS = 360, 808, 68, 26, 1.17, 10

P = json.load(open('project.json'))
font = ImageFont.truetype(FONT, SIZE)
try:
    font.set_variation_by_name('Bold')
except Exception:
    pass
img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
maxw = BOX_W - 80
lines = []
for part in P['hook'].replace('\\N', '\n').split('\n'):
    cur = ''
    for word in part.lstrip('~').split():
        test = (cur + ' ' + word).strip()
        if d.textlength(test, font=font) <= maxw or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
lh = int(SIZE * LINE)
box_h = len(lines) * lh + 2 * PADY
x0 = (1080 - BOX_W) // 2
d.rounded_rectangle([x0, TOP, x0 + BOX_W, TOP + box_h], radius=RADIUS, fill=(255, 255, 255, 255))
asc, desc = font.getmetrics()
for k, line in enumerate(lines):
    w = d.textlength(line, font=font)
    d.text(((1080 - w) / 2, TOP + PADY + k * lh + (lh - asc - desc) / 2), line, font=font, fill=(0, 0, 0, 255))
img.save('hook.png')
print('HOOK', lines, 'box', TOP, TOP + box_h)
