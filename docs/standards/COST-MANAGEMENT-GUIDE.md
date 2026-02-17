# Cost Management Guide

**Project:** Anny
**Last updated:** 2026-02-17

---

## Current Monthly Costs

| Resource | Provider | Cost | Notes |
|----------|----------|------|-------|
| Vultr VPS | Vultr | $6/mo | 1 vCPU, 1GB RAM, 25GB SSD |
| Domain/DNS | Existing infrastructure | $0 | anny.membies.com subdomain |
| SSL Certificate | Let's Encrypt | $0 | Auto-renewal via certbot |
| GA4 Data API | Google Cloud | $0 | Free, quota-based |
| Search Console API | Google Cloud | $0 | Free, no billing |
| Tag Manager API | Google Cloud | $0 | Free, no billing |
| GitHub | GitHub | $0 | Free tier (public repo) |
| CI/CD | GitHub Actions | $0 | Free tier (2,000 min/mo) |
| **Total** | | **$6/month** | |

## Cost Projections

### Current Scale (1 user, ~100 API calls/day)
- **Monthly:** $6
- **Annual:** $72

### Growth Triggers

| Trigger | Action | Cost Impact |
|---------|--------|-------------|
| Multiple users | Consider API key management | $0 (software change) |
| High traffic (>1000 req/day) | Upgrade VPS (2 vCPU, 2GB) | +$6/mo |
| Need for staging env | Second VPS | +$6/mo |
| Log aggregation needed | Grafana Cloud free tier or Loki | $0-30/mo |
| Uptime monitoring | UptimeRobot free tier | $0 |

## API Quotas (Not Costs)

All Google APIs are free. The constraint is quotas, not billing:

| API | Daily Quota | Rate Limit | Current Usage |
|-----|-------------|------------|--------------|
| GA4 Data API | 200,000 tokens | 40,000/hr | <1% |
| Search Console | 30,000,000 QPD | 1,200 QPM | <0.01% |
| Tag Manager | 10,000 requests | 25/100s | <0.1% |

## Cost Optimization

- No optimization needed at current scale
- If VPS upgrade is needed, consider switching to `docker compose` with resource limits before scaling hardware
- GitHub Actions free tier provides 2,000 minutes/month — more than sufficient for CI
