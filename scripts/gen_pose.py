#!/usr/bin/env python3
"""
キャラクターのポーズ・表情バリエーション生成
- 元キャラ画像を参考画像としてGeminiに送り、同じテイスト・同じ人物のまま
  ポーズ・表情だけを変えた画像を生成する。
- 背景は透過(or 白)で書き出し、Webで重ねやすくする。

使い方:
  python scripts/gen_pose.py            # TASKS をまとめて生成
出力: assets/characters/generated/<name>.png
"""
import sys, json, base64, urllib.request, urllib.error, os, io
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
ORIG = ROOT / "assets" / "characters" / "original"
OUT  = ROOT / "assets" / "characters" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

# ── .env ────────────────────────────────────────────────
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

MODELS = [
    "gemini-3-pro-image",
    "gemini-3-pro-image-preview",
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
]

STYLE_NOTE = (
    "添付した参考画像のキャラクターと【完全に同一人物】になるように描いてください。\n"
    "顔立ち・髪型・髪色・肌の色・服装(色とデザイン)・体型・頭身・画風を一切変えないこと。\n"
    "画風の特徴: 2.5〜3頭身のちびキャラ、水彩タッチの柔らかい塗り、"
    "茶系のラフな輪郭線、キャラの周囲を囲む白いステッカー風の縁取り。\n"
    "変えてよいのは『ポーズ』と『表情』だけです。\n"
    "全身を描き、背景は完全な透過(透明)にしてください。透過が無理なら純白の単色背景。\n"
    "文字・記号・ロゴ・吹き出しは一切入れないこと。"
)

def gen(src_name, pose, out_name):
    src = ORIG / src_name
    b64 = base64.b64encode(src.read_bytes()).decode()
    ref = {"inlineData": {"mimeType": "image/png", "data": b64}}
    prompt = f"{STYLE_NOTE}\n\n今回のポーズ・表情:\n{pose}"
    payload = json.dumps({
        "contents": [{"parts": [ref, {"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }).encode("utf-8")

    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        req = urllib.request.Request(url, data=payload,
              headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                result = json.loads(r.read())
            for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img = Image.open(io.BytesIO(base64.b64decode(part["inlineData"]["data"])))
                    dst = OUT / out_name
                    img.save(str(dst))
                    print(f"  OK [{model}] {src_name} -> {out_name} {img.size} {img.mode}")
                    return True
            print(f"  {model}: 画像なし → 次へ")
        except urllib.error.HTTPError as e:
            print(f"  {model}: HTTP {e.code} {e.read().decode()[:120]}")
        except Exception as e:
            print(f"  {model}: {e}")
    print(f"  失敗: {src_name} -> {out_name}")
    return False

# ── テスト生成タスク ─────────────────────────────────────
TASKS = [
    ("reception.png", "右手で横（画面の右方向）を指さして、こちらへどうぞと笑顔で案内するポーズ。", "reception_guide.png"),
    ("iwai.png", "右手の親指を立てて『おまかせください』とニッコリ自信のあるOKポーズ。", "iwai_thumbsup.png"),
    ("natsumi.png", "片手で首の後ろを押さえ、痛くて困った表情(眉を下げる)。むちうちで悩む患者の様子。", "natsumi_neckpain.png"),
]

if __name__ == "__main__":
    print(f"出力先: {OUT}")
    ok = 0
    for src, pose, out in TASKS:
        print(f"\n■ {src} → {out}")
        if gen(src, pose, out):
            ok += 1
    print(f"\n完了: {ok}/{len(TASKS)}")
