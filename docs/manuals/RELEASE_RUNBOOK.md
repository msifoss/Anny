# Release Runbook

**Project:** Anny
**Last updated:** 2026-02-17

---

## Pre-Release Checklist

- [ ] All tests pass (`make test`)
- [ ] Pylint 10/10 (`make lint`)
- [ ] `pip-audit` clean (`make audit`)
- [ ] Working tree clean (`git status`)
- [ ] CHANGELOG.md `[Unreleased]` section populated
- [ ] CLAUDE.md metrics current (test count, coverage, tool count)
- [ ] No open Critical or High security findings

## Release Steps

### 1. Update Version

```bash
# In pyproject.toml, update version
# In src/anny/main.py, update FastAPI version parameter
```

### 2. Update CHANGELOG

Move `[Unreleased]` contents to a new version header:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...
```

### 3. Commit and Tag

```bash
git add -A
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

### 4. Deploy

```bash
make deploy
```

### 5. Post-Deploy Verification

```bash
# Health check
curl https://anny.membies.com/health

# Smoke test
make smoke
```

## Documentation Sync Matrix

After every release, verify these are current:

| Document | Check |
|----------|-------|
| `CLAUDE.md` | Test count, coverage, tool count, status date |
| `README.md` | Feature list, setup instructions |
| `CHANGELOG.md` | Version entry with all changes |
| `SECURITY.md` | Audit status, known limitations |
| `pyproject.toml` | Version number matches tag |
| `src/anny/main.py` | FastAPI version parameter |
| `docs/REQUIREMENTS.md` | New requirements documented |
| `docs/TRACEABILITY-MATRIX.md` | New features traced to tests |
| `docs/standards/OPS-READINESS-CHECKLIST.md` | Score recalculated |

## Rollback Procedure

If a deploy causes issues:

```bash
# SSH to server
ssh deploy@anny.membies.com

# Check logs
cd /opt/anny && docker compose logs --tail 100

# Rollback to previous image (if available)
docker compose down
git checkout HEAD~1 -- Dockerfile src/ requirements.txt pyproject.toml
docker compose build && docker compose up -d
```

## Version History

| Version | Date | Tag | Notes |
|---------|------|-----|-------|
| 0.1.0 | 2026-02-13 | — | Initial scaffold |
| 0.2.0 | 2026-02-13 | — | GA4 + SC + GTM integrations |
| 0.3.0 | 2026-02-17 | — | Memory layer + deployment |
