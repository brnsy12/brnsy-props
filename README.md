# BRNSY PROPS

Mobile-first public NHL player-prop analytics dashboard.

## Setup
1. Upload all files/folders in this package to the root of `brnsy12/brnsy-props`.
2. Repository Settings → Pages → Source → **GitHub Actions**.
3. Get a SportsGameOdds API key.
4. Settings → Secrets and variables → Actions → New repository secret.
5. Name it exactly `SPORTSGAMEODDS_API_KEY` and paste the key.
6. Actions → **Update NHL prop data** → Run workflow.

Expected site: https://brnsy12.github.io/brnsy-props/

The preview rows are placeholders and are clearly labeled. The updater replaces them with real API data. Never commit an API key.

The initial live processor intentionally leaves L5/L10/L20/season blank until real historical results are persisted. Historical performance is descriptive, not a guarantee.
