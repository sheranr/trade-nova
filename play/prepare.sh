#!/bin/sh
# Copy the current Trade Nova app content into the Play build (play/app/src/main/assets).
# Same files as tools/build_apk.sh puts into the APK; only the native build number differs
# (read from play/app/build.gradle), so the "download new APK" banner never shows in the Play app.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
A="$ROOT/play/app/src/main/assets"
CODE=$(sed -n 's/^def PLAY_VERSION_CODE = \([0-9]*\).*/\1/p' "$ROOT/play/app/build.gradle")
[ -n "$CODE" ] || { echo "PLAY_VERSION_CODE not found"; exit 1; }
VER=$(python3 -c "import json;print(json.loads(json.load(open('$ROOT/docs/ota/version.json'))['payload'])['content'])")
BF=$(python3 -c "import hashlib,json;d='$ROOT/docs/';print(json.dumps({n:hashlib.sha256(open(d+n,'rb').read()).hexdigest() for n in ['index.html','hsdata.js','prices.js']},separators=(',',':')))")
rm -rf "$A"; mkdir -p "$A"
sed -e "s/__NATIVE_CODE__/$CODE/g" -e "s/__APP_VERSION__/$VER/" -e "s/__BUILTIN_FILES__/$BF/" "$ROOT/android/assets-src/boot.html" > "$A/index.html"
cp "$ROOT/docs/index.html" "$A/app.html"
cp "$ROOT/docs/hsdata.js" "$ROOT/docs/prices.js" "$A/"
cp -r "$ROOT/docs/pdf" "$A/pdf"
cp "$ROOT/docs/icons/icon-192.png" "$A/icon.png"
echo "Play assets ready (native $CODE, content $VER)"
