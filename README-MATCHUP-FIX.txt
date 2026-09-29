BRNSY PROPS — Matchup Fix

Replace ONLY:
scripts/process_props.py

Then:
1. Commit & Push to main.
2. GitHub → Actions → Update NHL prop data → Run workflow.
3. Wait for it to finish green.
4. Run Deploy BRNSY PROPS as a NEW workflow run if it does not deploy automatically.
5. Hard refresh the website.

This patch adds:
- matchup
- awayTeam
- homeTeam
- opponent (when inferable)

It does not change your API key or frontend files.
