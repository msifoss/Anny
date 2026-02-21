# No Active Bolt

Bolt 9 closed 2026-02-20. All items delivered, v0.8.0 deployed (deploy count: 8).

## Next Bolt Candidates

| # | Item | Size | Notes |
|---|------|------|-------|
| 22 | Multi-property support | M | Query across multiple GA4 properties |
| 21 | GTM workspace management (create/publish) | L | Requires write scopes |
| 27 | Conversion optimization audit tooling | M | Only 9/40+ content pages have CTAs |
| 28 | Social channel reactivation strategy | S | Organic social dropped 92% Q3→Q4 |

## Pending Actions

- ~~Deploy v0.8.0 to anny.membies.com~~ done
- ~~Verify rollback image tagging works on next deploy~~ done (89e8874073a1)
- ~~Run `scripts/backup.sh` on VPS and configure daily cron~~ done (daily 02:00 UTC)
- Fixed UFW: changed port 22 from LIMIT to ALLOW (fail2ban handles brute-force)
- Whitelisted deploy IP (142.59.68.61) in fail2ban
