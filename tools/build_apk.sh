#!/bin/sh
# Build and sign the Trade Nova Android app from this repository.
#   TN_TOOLS=dir-with-apktool.jar-and-signer.jar  TN_KEYSTORE=trademate-release.jks  TN_KEYPASS=...  tools/build_apk.sh out.apk
# apktool:   https://github.com/iBotPeaches/Apktool/releases   (saved as apktool.jar)
# signer:    https://github.com/patrickfav/uber-apk-signer/releases (saved as signer.jar)
# The keystore and passwords are kept outside the repository.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-$ROOT/TradeNova.apk}
W=$(mktemp -d)
cp -r "$ROOT/android" "$W/app"
A="$W/app/assets"; mkdir -p "$A"
CODE=$(sed -n 's/.*versionCode: \([0-9]*\).*/\1/p' "$ROOT/android/apktool.yml")
VER=$(python3 -c "import json;print(json.loads(json.load(open('$ROOT/docs/ota/version.json'))['payload'])['content'])")
sed -e "s/__NATIVE_CODE__/$CODE/" -e "s/__APP_VERSION__/$VER/" "$ROOT/android/assets-src/boot.html" > "$A/index.html"
rm -rf "$W/app/assets-src"
cp "$ROOT/docs/index.html" "$A/app.html"
cp "$ROOT/docs/hsdata.js" "$ROOT/docs/prices.js" "$A/"
cp -r "$ROOT/docs/pdf" "$A/pdf"
cp "$ROOT/docs/icons/icon-192.png" "$A/icon.png"
java -jar "$TN_TOOLS/apktool.jar" b "$W/app" -o "$W/unsigned.apk"
java -jar "$TN_TOOLS/signer.jar" -a "$W/unsigned.apk" -o "$W/out" --ks "$TN_KEYSTORE" --ksAlias trademate --ksPass "$TN_KEYPASS" --ksKeyPass "$TN_KEYPASS"
cp "$W"/out/*.apk "$OUT"
rm -rf "$W"
echo "Built $OUT (native $CODE, content $VER)"
