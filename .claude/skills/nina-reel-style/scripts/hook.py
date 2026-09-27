"""Render the hook title (first 3.2 s) as hook.png in Nina's Instagram style.

Uppercase rounded bold font (Fredoka), black text, each line on its own white
rounded box, centred. Top of the first box never above y=230 (Instagram top
UI zone). Lines come from project.json "hook" (split at \\N); a line starting
with "~" is drawn smaller (sub line, e.g. "Teil 2 (Platz 10 bis 6)").
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.expanduser('~/.fonts/Fredoka.ttf')
TOP, SIZE, SUB, PADX, PADY, GAP, RADIUS = 230, 88, 0.72, 30, 16, 0, 26

P = json.load(open('project.json'))
lines = [l for l in P['hook'].replace('\\N', '\n').split('\n') if l.strip()]
img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
y = TOP
for line in lines:
    sub = line.startswith('~')
    text = line.lstrip('~').upper()
    size = int(SIZE * (SUB if sub else 1))
    font = ImageFont.truetype(FONT, size)
    try:
        font.set_variation_by_axes([100, 650])  # width, weight (semi bold+)
    except Exception:
        pass
    while d.textlength(text, font=font) > 1080 - 2 * (PADX + 40):
        size -= 2
        font = font.font_variant(size=size)
    w = d.textlength(text, font=font)
    asc, desc = font.getmetrics()
    h = asc + desc
    x0 = (1080 - w) / 2 - PADX
    box = [x0, y, x0 + w + 2 * PADX, y + h + 2 * PADY]
    d.rounded_rectangle(box, radius=RADIUS, fill=(255, 255, 255, 255))
    d.text(((1080 - w) / 2, y + PADY), text, font=font, fill=(0, 0, 0, 255))
    y = box[3] + GAP
img.save('hook.png')
print('HOOK', lines, 'bottom', int(y))
