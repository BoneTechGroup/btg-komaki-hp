#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ブログ用アイキャッチ生成: Gemini Pro(キャラ参照・文字なし) + Pillowで日本語タイトル合成"""
import sys, json, base64, urllib.request, os, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
    line=line.strip()
    if line and not line.startswith("#") and "=" in line:
        k,_,v=line.partition("="); os.environ.setdefault(k.strip(),v.strip())
KEY=os.environ["GEMINI_API_KEY"]
FONT="C:/Windows/Fonts/NotoSansJP-VF.ttf"

REFS=[ROOT/"assets/イラスト/生成/iwai2.png", ROOT/"assets/イラスト/生成/natumi2.png"]
OUTDIR=ROOT/"assets/写真/blog"; OUTDIR.mkdir(parents=True, exist_ok=True)

def gen(scene, outname, title_lines):
    parts=[{"inlineData":{"mimeType":"image/png","data":base64.b64encode(r.read_bytes()).decode()}} for r in REFS]
    prompt=("ブログ用のアイキャッチ画像を生成してください。\n"
      "添付した2枚の参考画像のキャラクター(紺スクラブの男性スタッフ/私服の女性患者)と同一人物・同一画風で描くこと。\n"
      "画風: 2.5〜3頭身のちびキャラ、水彩タッチ、白フチのステッカー風、柔らかいパステル調の背景。\n"
      f"シーン: {scene}\n"
      "厳守事項:\n"
      "- 文字・数字・記号・ロゴ・透かしは一切入れない\n"
      "- 横長16:9の構図。キャラクターは右側に配置し、左側はテキスト用に明るい余白を残す\n"
      "- 背景は淡いパステル(ティファニーブルー系)で塗りつぶす")
    payload=json.dumps({"contents":[{"parts":parts+[{"text":prompt}]}],
      "generationConfig":{"responseModalities":["IMAGE","TEXT"]}}).encode()
    img=None
    for model in ["gemini-3-pro-image","gemini-3-pro-image-preview","gemini-3.1-flash-image"]:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
        req=urllib.request.Request(url,data=payload,headers={"Content-Type":"application/json; charset=utf-8"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=240) as r:
                res=json.loads(r.read())
            for part in res.get("candidates",[{}])[0].get("content",{}).get("parts",[]):
                if "inlineData" in part:
                    img=Image.open(io.BytesIO(base64.b64decode(part["inlineData"]["data"]))).convert("RGB")
                    print("OK",model,img.size); break
            if img: break
            print(model,"no image")
        except Exception as e: print(model,str(e)[:110])
    if not img: raise SystemExit("生成失敗")
    # 16:9にリサイズ・クロップ
    tw,th=1280,720
    sc=max(tw/img.width, th/img.height)
    img=img.resize((int(img.width*sc),int(img.height*sc)),Image.LANCZOS)
    l=(img.width-tw)//2; t=(img.height-th)//2
    img=img.crop((l,t,l+tw,t+th))
    # タイトル合成(ダーク文字+白ストローク・左寄せ)
    d=ImageDraw.Draw(img)
    fs=64 if len(title_lines)>=3 else 72
    font=ImageFont.truetype(FONT,fs)
    lh=font.getbbox("あ")[3]-font.getbbox("あ")[1]+14
    total=lh*len(title_lines)
    maxw=max(d.textbbox((0,0),ln,font=font)[2] for ln in title_lines)
    x,y0=52,(th-total)//2-8
    bg=Image.new("RGBA",img.size,(0,0,0,0))
    bd=ImageDraw.Draw(bg)
    bd.rounded_rectangle([(x-26,y0-18),(x+maxw+26,y0+total+18)],radius=16,fill=(255,255,255,150))
    img=Image.alpha_composite(img.convert("RGBA"),bg).convert("RGB")
    d=ImageDraw.Draw(img)
    y=y0
    for ln in title_lines:
        for dx in range(-4,5):
            for dy in range(-4,5):
                if dx or dy: d.text((x+dx,y+dy),ln,font=font,fill=(255,255,255))
        d.text((x,y),ln,font=font,fill=(38,56,58))
        y+=lh
    out=OUTDIR/outname
    img.save(out,"JPEG",quality=90)
    print("保存:",out)

if __name__=="__main__":
    gen("女性の患者が病院と接骨院の分かれ道の前で困った表情で立っている。"
        "隣で紺スクラブの男性スタッフが優しく片手を差し出して案内している。"
        "背景に病院の建物と接骨院の建物を淡くぼかして描く。",
        "eyecatch-blog1.jpg",
        ["交通事故のむちうち","病院と接骨院","どっちに行く？"])
