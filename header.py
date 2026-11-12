# Draws header.svg: a night mountain scene made of coloured ASCII characters.
# Run: python3 header.py > header.svg
import math, random
random.seed(4)
W, H = 104, 27
CW, CH = 7.8, 13          # one character cell, in px
cell = [[None] * W for _ in range(H)]   # (char, colour, class)

C = dict(snow='#b4c3f2', snowd='#7584cf', rock='#7477cc', rockd='#4c4d98', tree='#262f6a', treeedge='#34418a',
         grass='#7fe0f5', grassd='#2a8fb0', ground='#1d2a5c', haze='#3f98b8', star='#ffffff', name='#e8f0ff', sub='#9fb3e6')
F = dict(snow='#e1e9ff', snowd='#98a6e2', rock='#5a5cb0', rockd='#37387a', tree='#161c47', grass='#2b9fc4', ground='#0e1534')

def put(x, y, ch, col, cls='', fill=None):
    if 0 <= x < W and 0 <= y < H:
        cell[y][x] = (ch, col, cls, fill)

# Sky haze: dotted bands toward the horizon, like the picture's dithering.
for y in range(9, 17):
    step = max(1, 5 - (y - 9) // 2)
    for x in range(W):
        if (x + y * 2) % step == 0:
            put(x, y, '.' if y < 13 else ':', C['haze'])

def mountain(cx, top, ls, rs, snow, wob):
    for x in range(W):
        y0 = top + ((cx - x) / ls if x < cx else (x - cx) / rs)
        for y in range(max(0, math.ceil(y0)), 24):
            lit = x >= cx
            d = y - y0
            line = snow + wob * math.sin(x * 0.55) + wob * 0.6 * math.sin(x * 1.7)
            if d < line:
                ch = '#' if lit else '%'
                if lit and d < line - 1 and (x * 7 + y * 3) % 11 == 0: ch = '@'
                put(x, y, ch, C['snow'] if lit else C['snowd'], fill=F['snow'] if lit else F['snowd'])
            else:
                put(x, y, '=' if lit else ':', C['rock'] if lit else C['rockd'], fill=F['rock'] if lit else F['rockd'])

mountain(16, 11, 2.0, 2.2, 2.4, 0.7)
mountain(88, 9, 1.9, 2.4, 2.6, 0.7)
mountain(51, 3, 2.1, 2.6, 5.5, 1.2)

# Pines: narrow triangles with a lighter edge, packed into a forest.
x = -2
while x < W + 2:
    tip = random.randint(15, 20)
    for y in range(tip, 24):
        half = (y - tip + 1) // 2
        for dx in range(-half, half + 1):
            edge = abs(dx) == half
            put(x + dx, y, '^' if y == tip else ('/' if dx < 0 else '\\') if edge else 'A', C['treeedge'] if edge or y == tip else C['tree'], fill=F['tree'])
    x += random.choice([2, 3, 3, 4])

# Grass, then ground.
for x in range(W):
    put(x, 24, random.choice('"\',v"\''), C['grass'], fill=F['grass'])
    put(x, 25, random.choice(',.\'  '), C['grassd'], fill=F['ground'])
    put(x, 26, '.' if random.random() < 0.15 else ' ', C['ground'], fill=F['ground'])

# Stars (these twinkle).
for i, (x, y, ch) in enumerate([(3, 1, '*'), (12, 6, '.'), (22, 2, '+'), (30, 8, '.'), (38, 1, '*'), (60, 1, '.'),
                                 (66, 5, '+'), (74, 2, '*'), (81, 7, '.'), (93, 1, '+'), (99, 5, '*'), (8, 9, '+'), (70, 9, '.')]):
    put(x, y, ch, C['star'], f's s{i % 4}')

# Name, top left of the sky.
for row, (text, col) in enumerate([('MATT ERICKSON', C['name']), ('Infrastructure Engineer at Halo', C['sub']), ('Washington state', C['sub'])]):
    for j, ch in enumerate(text):
        put(4 + j, 2 + row, ch, col, 'n' if row == 0 else '')

esc = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'}
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W * CW:.0f} {H * CH}" width="{W * CW:.0f}" height="{H * CH}" role="img" aria-label="Matt Erickson, Infrastructure Engineer at Halo, Washington state. A night sky over snowy mountains and a pine forest, drawn in ASCII.">',
       '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
       '<stop offset="0" stop-color="#0a1033"/><stop offset="0.35" stop-color="#121d52"/>'
       '<stop offset="0.62" stop-color="#1b5d86"/><stop offset="0.9" stop-color="#121a45"/><stop offset="1" stop-color="#0c1230"/></linearGradient></defs>',
       '<style>text{font:12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre}'
       '.n{font-weight:700}.s{animation:tw 4s ease-in-out infinite}.s1{animation-delay:-1s}.s2{animation-delay:-2s}.s3{animation-delay:-3s}'
       '@keyframes tw{50%{opacity:.25}}@media (prefers-reduced-motion:reduce){.s{animation:none}}</style>',
       f'<rect width="100%" height="100%" fill="url(#sky)"/>']
for y in range(H):
    x = 0
    while x < W:
        f = cell[y][x] and cell[y][x][3]
        if not f:
            x += 1
            continue
        x2 = x
        while x2 + 1 < W and cell[y][x2 + 1] and cell[y][x2 + 1][3] == f:
            x2 += 1
        out.append(f'<rect x="{x * CW:.1f}" y="{y * CH}" width="{(x2 - x + 1) * CW:.1f}" height="{CH}" fill="{f}"/>')
        x = x2 + 1
for y in range(H):
    groups = {}
    for x in range(W):
        c = cell[y][x]
        if c and c[0].strip():
            groups.setdefault((c[1], c[2]), []).append((x, c[0]))
    for (col, cls), items in groups.items():
        xs = ' '.join(f'{x * CW:.1f}' for x, _ in items)
        chars = ''.join(esc.get(ch, ch) for _, ch in items)
        k = f' class="{cls}"' if cls else ''
        out.append(f'<text x="{xs}" y="{y * CH + 10}" fill="{col}"{k}>{chars}</text>')
out.append('</svg>')
print('\n'.join(out))
