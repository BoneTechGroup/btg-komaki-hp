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
    "全身を描き、背景は【完全な純白の単色】にしてください。\n"
    "背景にグリッド線・方眼・設計図/青写真のような線・スケッチの下書き線・影・模様を"
    "一切描かないこと(これは厳守)。\n"
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

# ── 生成タスク ───────────────────────────────────────────
TASKS = [
    # 受付・案内役
    ("reception.png", "両手を体の前で揃えて深くお辞儀している。にこやかな笑顔。お出迎えの挨拶。", "reception_bow.png"),
    ("reception.png", "片手で電話の受話器を耳に当て、もう片方の手で予約を受け付ける笑顔のポーズ。", "reception_phone.png"),
    # 患者・なつみさん
    ("natsumi.png", "両手の指先を頬に添えて不安そうに眉を下げた表情。事故後の不安や悩みを表す。", "natsumi_worry.png"),
    ("natsumi.png", "両手を胸の前で合わせ、目を細めて嬉しそう・安心した満面の笑顔。治療後の喜び。", "natsumi_happy.png"),
    # 岩井さん（眼鏡なし）
    ("iwai.png", "片手の手のひらを上に向けて差し出し、明るく説明・案内するポーズ。笑顔。", "iwai_explain.png"),
    ("iwai.png", "両手を体の前で揃えて丁寧にお辞儀している。誠実な笑顔。", "iwai_bow.png"),
    # 村瀬さん（丸眼鏡）
    ("murase.png", "人差し指を立ててポイントを解説するポーズ。優しい穏やかな笑顔。", "murase_point.png"),
    ("murase.png", "右手の親指を立てて『おまかせください』の自信あるOKポーズ。穏やかな笑顔。", "murase_thumbsup.png"),
    # 他店舗スタッフ
    ("staff1.png", "片手を上げて元気に手を振って挨拶しているポーズ。明るい笑顔。", "staff1_wave.png"),
    ("staff2.png", "片手の手のひらを上に向けて差し出し、こちらへどうぞと案内するポーズ。笑顔。", "staff2_guide.png"),
]

if __name__ == "__main__":
    print(f"出力先: {OUT}")
    ok = 0
    for src, pose, out in TASKS:
        print(f"\n■ {src} → {out}")
        if gen(src, pose, out):
            ok += 1
    print(f"\n完了: {ok}/{len(TASKS)}")
