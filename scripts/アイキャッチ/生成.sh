#!/bin/bash
# ============================================================
# 事故ブログ アイキャッチ生成スクリプト
# 使い方:
#   bash 生成.sh 出力名.png "1行目" "2行目" "3行目(省略可)" [キャラ画像名]
# 例:
#   bash 生成.sh eyecatch2.png "交通事故に遭った直後" "その場でやるべき【5つのこと】" "" uketuke1.png
# ※【】で囲むとその部分がティファニー色の強調になる
# ============================================================
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$1"; L1="$2"; L2="$3"; L3="$4"; CHAR="${5:-uketuke1.png}"
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"

enc() {
  local LC_ALL=C s="$1" out="" c i n
  for ((i=0; i<${#s}; i++)); do
    c="${s:i:1}"
    case "$c" in
      [a-zA-Z0-9.~_-]) out+="$c" ;;
      *) n=$(printf '%d' "'$c"); ((n<0)) && ((n+=256)); printf -v c '%%%02X' "$n"; out+="$c" ;;
    esac
  done
  printf '%s' "$out"
}

Q="l1=$(enc "$L1")&l2=$(enc "$L2")&char=$(enc "$CHAR")"
[ -n "$L3" ] && Q="$Q&l3=$(enc "$L3")"

WIN_DIR=$(cygpath -w "$DIR" | sed 's|\\|/|g')
"$CHROME" --headless --disable-gpu --screenshot="$(cygpath -w "$DIR/$OUT")" \
  --window-size=1200,630 --hide-scrollbars \
  "file:///$WIN_DIR/テンプレ.html?$Q" 2>/dev/null
echo "生成完了: $DIR/$OUT"
