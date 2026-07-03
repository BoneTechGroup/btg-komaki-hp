#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""事故事例タイル用のシーンイラスト9枚を生成(ちびキャラ水彩・文字なし・純白背景)"""
import sys, json, base64, urllib.request, os, io
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
    line=line.strip()
    if line and not line.startswith("#") and "=" in line:
        k,_,v=line.partition("="); os.environ.setdefault(k.strip(),v.strip())
KEY=os.environ["GEMINI_API_KEY"]

REFS=[ROOT/"assets/イラスト/生成/iwai2.png", ROOT/"assets/イラスト/生成/natumi2.png"]
OUT=ROOT/"assets/イラスト/事例"; OUT.mkdir(parents=True, exist_ok=True)

STYLE=("添付した参考画像と同じ画風で描いてください。\n"
 "画風: 水彩タッチの柔らかい塗り、茶系のラフな輪郭線、パステル調、可愛いデフォルメ。\n"
 "構図: 正方形(1:1)のアイコン向けイラスト。シンプルで一目で状況が分かること。\n"
 "厳守: 文字・数字・記号・ロゴ・透かしは一切入れない。血や怪我の生々しい描写はしない。"
 "背景は完全な純白の単色。市松模様・グリッド・影は描かない。")

SCENES=[
 ("tsuitotsu","停車中の可愛いデフォルメの水色の車に、後ろから来たオレンジの車が追突した瞬間。衝撃マークを車の間に。"),
 ("kousaten","交差点で2台のデフォルメの車が出会い頭にぶつかりそうな俯瞰シーン。信号機を1つ添える。"),
 ("tamatsuki","3台のデフォルメの車が縦に連なって玉突き衝突しているシーン。横から見た構図。"),
 ("chushajo","駐車場の白線の中で、バックしてきたデフォルメの車が別の車にぶつかったシーン。"),
 ("jitensha","自転車に乗ったちびキャラの女性と、デフォルメの車が接触しそうなシーン。"),
 ("bike","原付バイクに乗ったちびキャラ(ヘルメット着用)と、デフォルメの車が接触しそうなシーン。"),
 ("hokousha","横断歩道を歩くちびキャラの女性と、近づくデフォルメの車。歩行者は驚いた表情。"),
 ("kodomo","車の後部座席のチャイルドシートに座る可愛いちびキャラの子供。少し不安そうな表情。"),
 ("ninpu","お腹の大きな妊婦のちびキャラ女性が車の助手席でシートベルトを着けて座り、お腹に手を添えて心配そうな表情。"),
]

def gen(slug, scene):
    parts=[{"inlineData":{"mimeType":"image/png","data":base64.b64encode(r.read_bytes()).decode()}} for r in REFS]
    parts.append({"text":f"{STYLE}\n\n今回のシーン: {scene}"})
    payload=json.dumps({"contents":[{"parts":parts}],
      "generationConfig":{"responseModalities":["IMAGE","TEXT"]}}).encode()
    for model in ["gemini-3-pro-image","gemini-3-pro-image-preview","gemini-3.1-flash-image"]:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
        req=urllib.request.Request(url,data=payload,headers={"Content-Type":"application/json; charset=utf-8"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=240) as r:
                res=json.loads(r.read())
            for part in res.get("candidates",[{}])[0].get("content",{}).get("parts",[]):
                if "inlineData" in part:
                    (OUT/f"{slug}.png").write_bytes(base64.b64decode(part["inlineData"]["data"]))
                    print(f"  OK [{model}] {slug}")
                    return True
            print(f"  {model}: no image")
        except Exception as e:
            print(f"  {model}: {str(e)[:100]}")
    print(f"  失敗: {slug}")
    return False

if __name__=="__main__":
    ok=0
    for slug,scene in SCENES:
        print(f"■ {slug}")
        ok+=gen(slug,scene)
    print(f"完了 {ok}/{len(SCENES)}")
