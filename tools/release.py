#!/usr/bin/env python3
"""Publish a Trade Nova update.

  python3 tools/release.py --version 2.0.1 --notes "What changed" --key /path/ota-signing-private.pem
      [--min-native 14] [--apk path/to/TradeNova.apk --apk-code 15 --apk-version 2.1.0]

What it does
  1. Builds docs/index.html from src/app.html (stamps the version).
  2. Builds docs/sw.js so web / PWA users get the update.
  3. Writes docs/ota/version.json, signed with the private OTA key, so installed
     Android apps download and verify the update (index.html, hsdata.js, prices.js).
  4. Optionally publishes a new APK to docs/download/ and tells older apps to install it.
Then commit and push; GitHub Pages serves the update within a minute or two.
The private key must never be committed to this repository.
"""
import argparse, base64, hashlib, json, os, re, shutil, datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
OTA_FILES = ['index.html', 'hsdata.js', 'prices.js']

ap = argparse.ArgumentParser()
ap.add_argument('--version', required=True)
ap.add_argument('--notes', default='')
ap.add_argument('--key', default=os.environ.get('TN_OTA_KEY', ''))
ap.add_argument('--min-native', type=int)
ap.add_argument('--apk'); ap.add_argument('--apk-code', type=int); ap.add_argument('--apk-version')
a = ap.parse_args()
if not re.fullmatch(r'\d+\.\d+\.\d+', a.version): raise SystemExit('version must look like 2.0.1')
if not a.key or not os.path.exists(a.key): raise SystemExit('give --key (the private OTA signing key, kept outside the repo)')

app = open(os.path.join(ROOT, 'src', 'app.html'), encoding='utf-8').read()
open(os.path.join(DOCS, 'index.html'), 'w', encoding='utf-8').write(app.replace('__APP_VERSION__', a.version))
sw = open(os.path.join(ROOT, 'tools', 'sw.template.js'), encoding='utf-8').read()
open(os.path.join(DOCS, 'sw.js'), 'w', encoding='utf-8').write(sw.replace('__APP_VERSION__', a.version))

prev = {}
vf = os.path.join(DOCS, 'ota', 'version.json')
if os.path.exists(vf): prev = json.loads(json.load(open(vf))['payload'])

apk = prev.get('apk')
if a.apk:
    os.makedirs(os.path.join(DOCS, 'download'), exist_ok=True)
    shutil.copy(a.apk, os.path.join(DOCS, 'download', 'TradeNova.apk'))
    apk = {'code': a.apk_code, 'version': a.apk_version,
           'url': 'https://sheranr.github.io/trade-nova/download/TradeNova.apk',
           'page': 'https://sheranr.github.io/trade-nova/download/',
           'sha256': hashlib.sha256(open(a.apk, 'rb').read()).hexdigest(),
           'size': os.path.getsize(a.apk)}

files = {}
for n in OTA_FILES:
    b = open(os.path.join(DOCS, n), 'rb').read()
    files[n] = {'sha256': hashlib.sha256(b).hexdigest(), 'size': len(b)}
payload = {'app': 'trade-nova', 'content': a.version, 'notes': a.notes,
           'minNative': a.min_native if a.min_native is not None else prev.get('minNative', 14),
           'apk': apk, 'files': files,
           'released': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
ptxt = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
key = serialization.load_pem_private_key(open(a.key, 'rb').read(), password=None)
der = key.sign(ptxt.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
r, s = utils.decode_dss_signature(der)
sig = base64.b64encode(r.to_bytes(32, 'big') + s.to_bytes(32, 'big')).decode()
os.makedirs(os.path.dirname(vf), exist_ok=True)
json.dump({'payload': ptxt, 'sig': sig}, open(vf, 'w'), ensure_ascii=False)

# keep the download page's version text in step
dp = os.path.join(DOCS, 'download', 'index.html')
if os.path.exists(dp) and apk:
    t = open(dp, encoding='utf-8').read()
    t = re.sub(r'<b id="apkv">.*?</b>', f'<b id="apkv">{apk["version"]}</b>', t)
    t = re.sub(r'<span id="apks">.*?</span>', f'<span id="apks">{apk["size"]/1e6:.0f} MB</span>', t)
    open(dp, 'w', encoding='utf-8').write(t)
print('Release', a.version, 'ready:', {k: v['sha256'][:12] for k, v in files.items()}, '| APK', apk and apk['version'])
