#!/usr/bin/env python3
"""四隅の背景色を自動サンプルし、その色に近い外周ピクセルだけを
フラッドフィルで透過化する。背景が明(白)でも暗(黒)でも対応。
キャラの輪郭線(背景と異なる色)でフィルが止まり内部は保護される。"""
import sys, os
from pathlib import Path
from collections import deque
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
GEN = Path(__file__).parent.parent / "assets" / "characters" / "generated"
DIST = 50  # 背景サンプル色からの許容距離

def sample_bg(px, w, h):
    cs = []
    for (x, y) in [(2,2),(w-3,2),(2,h-3),(w-3,h-3),(w//2,2),(w//2,h-3),(2,h//2),(w-3,h//2)]:
        p = px[x, y]
        cs.append((p[0], p[1], p[2]))
    return cs

def near_bg(px, samples):
    r, g, b = px[0], px[1], px[2]
    for (sr, sg, sb) in samples:
        if abs(r-sr)+abs(g-sg)+abs(b-sb) <= DIST:
            return True
    return False

def knockout(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    px = img.load()
    samples = sample_bg(px, w, h)
    seen = [[False]*w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if px[x,y][3] and near_bg(px[x,y], samples) and not seen[y][x]:
                seen[y][x]=True; q.append((x,y))
    for y in range(h):
        for x in (0, w-1):
            if px[x,y][3] and near_bg(px[x,y], samples) and not seen[y][x]:
                seen[y][x]=True; q.append((x,y))
    while q:
        x, y = q.popleft()
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and not seen[ny][nx] and px[nx,ny][3] and near_bg(px[nx,ny], samples):
                seen[ny][nx]=True; q.append((nx,ny))
    img.save(path)
    trans = sum(1 for yy in range(0,h,9) for xx in range(0,w,9) if px[xx,yy][3]==0)
    tot = len(range(0,h,9))*len(range(0,w,9))
    return img.size, round(trans/tot,2)

if __name__ == "__main__":
    files = sys.argv[1:] or [str(GEN/f) for f in os.listdir(GEN) if f.endswith(".png")]
    for f in files:
        size, ratio = knockout(f)
        print(f"  透過化: {os.path.basename(f)} {size} 透過率{ratio}")
    print("完了")
