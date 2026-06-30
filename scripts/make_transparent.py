#!/usr/bin/env python3
"""黒背景のキャラ画像を透過PNGに変換する。
白いステッカー縁取りより外側の黒を透明にする(フラッドフィル方式)。
元画像は original/_raw/ にバックアップ。"""
import sys
from pathlib import Path
from collections import deque
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ORIG = Path(__file__).parent.parent / "assets" / "characters" / "original"
RAW = ORIG / "_raw"
RAW.mkdir(exist_ok=True)

TARGETS = ["iwai.png", "murase.png"]
THRESH = 60  # この明るさ以下を黒背景候補とする

def is_dark(px):
    return px[0] < THRESH and px[1] < THRESH and px[2] < THRESH

def remove_black_bg(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    px = img.load()
    visited = [[False]*w for _ in range(h)]
    q = deque()
    # 四辺の暗いピクセルから外側の黒だけをフラッドフィル(キャラ内の黒は残す)
    for x in range(w):
        for y in (0, h-1):
            if is_dark(px[x, y]) and not visited[y][x]:
                q.append((x, y)); visited[y][x] = True
    for y in range(h):
        for x in (0, w-1):
            if is_dark(px[x, y]) and not visited[y][x]:
                q.append((x, y)); visited[y][x] = True
    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx] and is_dark(px[nx, ny]):
                visited[ny][nx] = True; q.append((nx, ny))
    return img

for name in TARGETS:
    p = ORIG / name
    if not p.exists():
        print(f"  skip (なし): {name}"); continue
    Image.open(p).save(RAW / name)        # バックアップ
    out = remove_black_bg(p)
    out.save(p)
    print(f"  透過化: {name} ({out.size})")
print("完了")
