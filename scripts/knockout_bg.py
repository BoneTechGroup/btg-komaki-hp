#!/usr/bin/env python3
"""生成画像(暗い背景)を外周フラッドフィルで透過化。
キャラ周囲の明るい白フチがバリアになり内部(紺スクラブ等の暗部)は保護される。
※ Geminiは参考画像の背景に関わらず暗背景で出力するため、暗背景除去で統一できる。"""
import sys, os
from pathlib import Path
from collections import deque
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
GEN = Path(__file__).parent.parent / "assets" / "characters" / "generated"
THRESH = 100  # 明るさ(最大チャンネル)がこれ未満=暗背景候補

def dark(px):
    return max(px[0], px[1], px[2]) < THRESH

def knockout(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    px = img.load()
    seen = [[False]*w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if dark(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w-1):
            if dark(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and dark(px[nx, ny]):
                seen[ny][nx] = True; q.append((nx, ny))
    img.save(path)
    trans = sum(1 for yy in range(0, h, 9) for xx in range(0, w, 9) if px[xx, yy][3] == 0)
    tot = len(range(0, h, 9)) * len(range(0, w, 9))
    return img.size, round(trans/tot, 2)

if __name__ == "__main__":
    files = sys.argv[1:] or [str(GEN / f) for f in os.listdir(GEN) if f.endswith(".png")]
    for f in files:
        size, ratio = knockout(f)
        print(f"  透過化: {os.path.basename(f)} {size} 透過率{ratio}")
    print("完了")
