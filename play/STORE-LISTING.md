# Trade Nova — Google Play listing and Play Console answers

Copy these into Play Console. Text limits are shown in brackets.

## Store listing

**App name** (30): `Trade Nova: HS Codes & Trade`

**Short description** (80):
`HS code lookup, duty estimator and trade finance tools for Sri Lanka.`

**Full description** (4000):

```
Trade Nova — Smarter Trade. Greater Confidence.

A free reference app for trade finance, imports and exports in Sri Lanka — built for bank trade finance teams, importers, exporters and anyone who works with HS codes.

HS CODE LOOKUP & DUTY ESTIMATOR
• Search all 9,007 tariff lines of the Sri Lanka Customs National Imports Tariff Guide 2026 by product words or HS code
• Duty, VAT, PAL, CESS, excise, SSCL and Special Commodity Levy rates in one place
• Import control status from the Consolidated Import Control List
• Works offline — the full tariff guide is inside the app

TRADE FINANCE DESKS
• Imports and Exports desks with practical guidance
• Circulars and gazettes library with links to the official sources
• Alerts and a personal watchlist of HS codes
• Payment tracker links for cross-border payments

RISK & PRICE CHECKS
• Sanctions & TBML awareness: country check, vessel check by name or IMO, red flags
• World price check (World Bank commodity prices) and invoice price check (UN Comtrade data)

LEARNING
• Learning Hub with training videos
• English articulation practice

PRIVATE BY DESIGN
No sign-in, no ads, no tracking. What you save stays on your phone. Content updates arrive automatically when you are online.

DATA SOURCES
• Sri Lanka Customs — National Imports Tariff Guide 2026, SCL chart: https://www.customs.gov.lk/
• Import & Export Control Department — Consolidated Import Control List: https://imexport.gov.lk/
• Government gazettes (Department of Government Printing): https://www.documents.gov.lk/
• Central Bank of Sri Lanka and Department of Foreign Exchange: https://www.cbsl.gov.lk/ · https://www.dfe.lk/
• Financial Intelligence Unit Sri Lanka: https://fiusrilanka.gov.lk/
• World Bank Commodity Price Data and UN Comtrade

DISCLAIMER
Trade Nova is an independent app created by Sheran Rajaguru. It is not affiliated with, endorsed by or representing Sri Lanka Customs, the Government of Sri Lanka, the Central Bank of Sri Lanka or any bank. Information is provided for reference only. Always confirm HS classification, rates and import conditions with the official sources and Sri Lanka Customs before acting; the official source prevails. Bank names are shown only as links to their public websites.
```

**App category:** Business  **Tags:** Business, Reference
**Contact email:** your developer email (shown publicly) · **Phone (optional):** 070 212 8617 · **Website:** https://sheranr.github.io/trade-nova/
**Privacy policy URL:** https://sheranr.github.io/trade-nova/privacy.html

**Graphics**
- App icon 512 × 512 PNG (current Trade Nova icon)
- Feature graphic 1024 × 500 (can be made from the landscape start-screen artwork)
- Phone screenshots: at least 2 (suggest 4–6: Home, HS lookup result, duty estimator, Learning Hub, Sanctions & TBML). 7" and 10" tablet screenshots are optional but help, since the app has a tablet layout.

## App content (Policy → App content)

| Form | Answer |
|---|---|
| Privacy policy | https://sheranr.github.io/trade-nova/privacy.html |
| App access | All functionality is available without special access (no login) |
| Ads | No, my app does not contain ads |
| Content rating | Category: Reference, News or Educational. Answer No to all violence, sexual, language, drugs, gambling questions. User interaction: No. Shares location: No. Expected rating: Everyone / 3+ |
| Target audience | 18 and over only. Not designed for children |
| News app | No |
| Data safety | Does your app collect or share user data? **No.** (Data stays on the device; content downloads send no personal data. Encryption in transit: Yes — all downloads use HTTPS. Account deletion: not applicable — no accounts) |
| Government apps | No — not developed by or on behalf of a government |
| Financial features | My app doesn't provide any financial features (it's a reference app; no loans, payments, banking or trading) |
| Health apps | My app does not have any health features |
| Advertising ID | No |

## Closed test (needed before production)
1. Testing → Closed testing → create a track, upload the signed .aab, add a Google Group or email list with at least 12 testers.
2. Send testers the opt-in link. They tap "Become a tester", then install Trade Nova from Play (not the APK).
3. Keep at least 12 testers opted in for 14 days in a row. Ask them to open the app a few times and send feedback.
4. Then: Dashboard → Apply for production → answer the questions about the test.

Note for testers who already have the APK: the Play version replaces it only if Play signs with the same `trademate` key (see Play App Signing below). Otherwise they need to uninstall the APK first.

## Play App Signing — keep the existing key
When you create the first release, Play asks how to sign the app. Choose **"Use a different key" → "Export and upload a key from Java keystore"**, download the PEPK tool and Google's encryption key shown there, and export the `trademate` key. Then phones that already have the APK can update to the Play version without uninstalling.
