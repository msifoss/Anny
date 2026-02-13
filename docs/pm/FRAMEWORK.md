# Anny Sprint Framework — Bolts

> "Good process is as lightweight as possible, while being rigorous enough to consistently work."

## Why "Bolts"?

A Bolt is a short, concentrated sprint optimized for a solo developer working with an AI pair. No standups, no ceremonies — just focused building with lightweight tracking to stay honest about progress.

## Cadence

```
Monday    → Bolt Planning (15 min)
Tue–Thu   → Build
Friday    → Bolt Review + Retro (15 min)
```

## Metrics

| Metric | What It Measures |
|--------|-----------------|
| Commits | Volume of shippable work |
| Tests Δ | Net change in test count |
| Deploys | Production deployments |
| Blocked % | Days blocked / total days |

## Velocity

T-shirt sizes for estimation:

| Size | Time | Example |
|------|------|---------|
| S | < 1 hour | Add a config option, fix a typo |
| M | < half day | New endpoint, add validation |
| L | ~ 1 day | New feature module, refactor |
| XL | Multi-day | Major feature, architecture change |

## Handling External Blockers

1. Separate blocked from executable
2. File tickets immediately
3. Pivot, don't wait
4. Track blocked-time %
5. Follow up weekly

## Artifacts

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| FRAMEWORK.md | How we work | Rarely |
| CURRENT-SPRINT.md | Active Bolt status | Daily |
| SPRINT-LOG.md | Archive of completed Bolts | Weekly |
| BACKLOG.md | Prioritized product backlog | Weekly |
