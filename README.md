# BTG接骨院 小牧院 — 交通事故専門サイト制作

BTG接骨院 小牧院の交通事故・むち打ち専門サイト。
ブログ自動化プロジェクト（seo-automation）とは**完全に別管理**。

参考デザイン：[ねこのて行政書士事務所](https://www.neconote-office.com/) ／ 系列：[jiko-ichinomiya.com](https://jiko-ichinomiya.com/)

---

## 🌐 公開URL（GitHub Pages・noindex中）

**https://bonetechgroup.github.io/btg-komaki-hp/**

- `main` に push すると1〜2分で自動反映される。
- 確認・共有用のため `noindex,nofollow`＋robots.txt で検索よけ済み。独自ドメイン取得後に解除する。
- 無料公開のためリポジトリは**public**（ソース公開）。ソースを隠したい場合はCloudflare Pagesへ移行可。

## 🏠 家のPCで続きを始める手順

```bash
# 1. リポジトリを取得
git clone https://github.com/BoneTechGroup/btg-komaki-hp.git
cd btg-komaki-hp

# 2. サイトを見る（どちらでもOK）
#  ・index.html をダブルクリックしてブラウザで開く
#  ・または簡易サーバー: python -m http.server 5500 → http://localhost:5500/
```

### Geminiでキャラのポーズを追加生成したい場合のみ
`.env` は秘密情報のためGitに含まれません。手動で作成してください：
```
GEMINI_API_KEY=（Google AI StudioのAPIキー）
```
（サイトを見るだけ・文章や色の編集だけなら `.env` は不要です）

---

## ✅ 現在の進捗（ここまで完成）

- **トップページ（1ページLP）完成**：`index.html`
  - ヒーロー／お悩み／自賠責0円／選ばれる7理由／施術の流れ／スタッフ紹介／
    院の雰囲気（写真ギャラリー）／料金・慰謝料／FAQ／アクセス／CTA
- **テーマカラー**：ティファニーブルー（`--tiffany:#0ABAB5`）
- **動き**：スクロール出現アニメ、キャラ浮遊、背景ブロブ変形、ホバー、
  FAQアコーディオン、写真ライトボックス、スマホ追従バー
- **SEO/AEO**：title/meta/OGP、構造化データ（MedicalBusiness + FAQPage）
- **キャラクター**：6名分の原画＋ポーズ生成（透過処理済み）
- **院内写真**：実際の写真をWeb最適化して掲載

## 📁 フォルダ構成

```
index.html                       … トップページ本体
assets/css/style.css             … デザイン（ティファニーブルー）
assets/js/main.js                … アニメ/FAQ/ライトボックス/メニュー
assets/characters/original/      … キャラ原画(6名) ※iwai/murase透過済み, _raw=元
assets/characters/generated/     … Geminiで生成したポーズ(透過済み)
assets/photos/                   … 院内・施術写真(Web最適化済み)
scripts/gen_pose.py              … キャラのポーズ生成(要 .env のGEMINIキー)
scripts/knockout_bg.py           … 暗背景を透過(白フチをバリアに内部保護)
scripts/knockout_auto.py         … 四隅の背景色を自動判定して透過(明/暗両対応)
SITE_INFO.md                     … 院の確定情報(住所/電話/営業時間/スタッフ)
```

## 🎨 キャラクター方針（崩さない）

ちびキャラ・紺スクラブ（受付/患者は私服）・水彩タッチ・白フチのステッカー風。
プロのイラストレーター依頼を予定。ポーズ追加は `scripts/gen_pose.py` の
`TASKS` に追記して実行 → `knockout_auto.py` で背景透過。

---

## 📝 次にやること（候補・未着手）

- [ ] 実スタッフ写真（岩井/村瀬）の活用（※元写真に文字入り。素の写真があれば差替え）
- [ ] 院紹介の動画（.mov 3本）をヒーロー等に活用するか検討
- [ ] キャッチコピー・文言の最終調整
- [ ] 「お客様の声」セクション追加
- [ ] スマホ表示の最終チェック
- [ ] 他店舗スタッフ（staff1/staff2）の登場
- [ ] 生成画像の隅に残る小さな星マーク（✦）の除去
- [ ] ドメイン取得・公開（静的サイトなのでGitHub Pages等で無料公開可）

## 連絡先・院情報

詳細は `SITE_INFO.md` を参照。
電話 0568-90-1841 ／ LINE https://lin.ee/XPgv3I6 ／
〒485-0058 愛知県小牧市小木1丁目112 プローグ小木II 1F
