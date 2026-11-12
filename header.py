# Draws header.svg: a quiet night over the mountains, in coloured ASCII.
# Run: python3 header.py > header.svg
W, H = 96, 15
CW, CH = 7.8, 14          # one character cell, in px
cell = [[None] * W for _ in range(H)]   # (char, colour, class)
C = dict(ridge='#9aa6e0', snow='#e8f0ff', rock='#4b5390', tree='#3d6f8f', ground='#2a3a6a',
         star='#ffffff', name='#e8f0ff', sub='#8f9fd6')

def put(x, y, ch, col, cls=''):
    if 0 <= x < W and 0 <= y < H:
        cell[y][x] = (ch, col, cls)

# Peaks, back to front: (centre column, top row, rows of snow). Slopes are one column per row.
BASE = 12
for cx, top, snow in [(6, 7, 1), (90, 7, 1), (21, 5, 2), (76, 4, 2), (35, 4, 2), (62, 3, 3), (48, 1, 4)]:
    for y in range(top, BASE + 1):
        r = y - top
        for x in range(cx - r, cx + r + 1):
            put(x, y, ' ', None)                     # hide whatever is behind
        if r == 0:
            put(cx, y, '^', C['snow'])
            continue
        put(cx - r, y, '/', C['ridge'])
        put(cx + r, y, '\\', C['ridge'])
        for x in range(cx - r + 1, cx + r):
            if r <= snow:
                put(x, y, '.' if (x + y) % 2 else ':', C['snow'])
            elif (x * 3 + y) % 7 == 0:
                put(x, y, '.', C['rock'])

# One row of pines along the bottom, and the ground.
for x in range(W):
    put(x, BASE + 1, 'A' if x % 5 in (0, 2) else '^', C['tree'])
    put(x, BASE + 2, '_' if x % 2 else '-', C['ground'])

# Stars (these twinkle).
for i, (x, y) in enumerate([(2, 0), (40, 1), (56, 0), (69, 1), (84, 2), (93, 0), (12, 5), (27, 3), (89, 5)]):
    put(x, y, '*' if i % 3 == 0 else '+' if i % 3 == 1 else '.', C['star'], f's s{i % 4}')

# Name, top left.
for row, (text, col) in enumerate([('MATT ERICKSON', C['name']), ('Infrastructure Engineer at Halo', C['sub']), ('Washington state', C['sub'])]):
    for j, ch in enumerate(text):
        put(4 + j, 1 + row, ch, col, 'n' if row == 0 else '')

esc = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W * CW:.0f} {H * CH}" width="{W * CW:.0f}" height="{H * CH}" role="img" '
       'aria-label="Matt Erickson, Infrastructure Engineer at Halo, Washington state. Snowy mountains under the stars, drawn in ASCII.">',
       '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1030"/><stop offset="1" stop-color="#16245a"/></linearGradient></defs>',
       '<style>text{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre}'
       '.n{font-weight:700}.s{animation:tw 4s ease-in-out infinite}.s1{animation-delay:-1s}.s2{animation-delay:-2s}.s3{animation-delay:-3s}'
       '@keyframes tw{50%{opacity:.25}}@media (prefers-reduced-motion:reduce){.s{animation:none}}</style>',
       '<rect width="100%" height="100%" rx="8" fill="url(#sky)"/>']
for y in range(H):
    groups = {}
    for x in range(W):
        c = cell[y][x]
        if c and c[0].strip():
            groups.setdefault((c[1], c[2]), []).append((x, c[0]))
    for (col, cls), items in groups.items():
        xs = ' '.join(f'{(x + 0.5) * CW:.1f}' for x, _ in items)
        k = f' class="{cls}"' if cls else ''
        out.append(f'<text x="{xs}" y="{y * CH + 11}" fill="{col}"{k}>{"".join(esc.get(ch, ch) for _, ch in items)}</text>')
out.append('</svg>')
print('\n'.join(out))
