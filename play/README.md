# Trade Nova — Google Play build

This folder builds the Google Play version of Trade Nova. It is separate from everything else:

| Keeps working exactly as before | Where |
|---|---|
| Sideloaded APK (staff phones) + "new version" banner | `android/`, `tools/build_apk.sh`, GitHub Release |
| Web app / PWA (iPhone, computers) | `docs/` on GitHub Pages |
| OTA content updates | `docs/ota/` — the Play app receives them too |
| Admin page (videos, notices) | `docs/admin/` — the Play app shows the same live content |

## What is different in the Play build
- Targets Android 16 (API 36), as Google Play requires for new apps; built as an App Bundle (.aab).
- Same package (`lk.trademate.hs`) so phones with the APK can update from Play — only if Play signs with the same `trademate` key.
- Native build number 100+ (APK uses < 100), so the "download new APK" banner never shows in the Play app. Play delivers app updates.
- Edge-to-edge screens (Android 15+) and predictive Back (Android 16) handled.
- Web links always open in the browser, never inside the app.

## Build
Push to the `play-store` branch (or run "Build Google Play bundle" in Actions).
The workflow takes the latest app content from `main`, builds, and attaches:
- `trade-nova-play-aab` — unsigned .aab → sign with the upload key, upload to Play Console
- `trade-nova-play-test` — "Trade Nova (test)" APK for a quick check on a phone

Sign the bundle (keystore kept outside the repo):

    jarsigner -sigalg SHA256withRSA -digestalg SHA-256 -keystore trademate-release.jks app-release.aab trademate

## Every new Play upload
1. Raise `PLAY_VERSION_CODE` in `play/app/build.gradle` (100 → 101 …) and `PLAY_VERSION_NAME` if you like.
2. Push to `play-store`, sign, upload.

Content-only changes (HS data, videos, notices, screens) don't need a Play upload — OTA and the admin page deliver them.
If a future APK adds new native features, add them here too before raising `minNative` in an OTA release.
