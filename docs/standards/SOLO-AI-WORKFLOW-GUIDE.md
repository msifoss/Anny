# Solo + AI Development Workflow Guide

**Project:** Anny
**Last updated:** 2026-02-17

---

## Overview

Anny is developed by a solo developer paired with AI (Claude Code). This guide documents the workflow patterns, quality gates, and cadence that keep the project moving without a team.

## Bolt Cadence

- **Bolt = 1-week sprint** with a single goal statement
- Bolts are numbered sequentially (Bolt 1, 2, 3...)
- Each Bolt has 3-6 items sized S/M/L/XL
- Close a Bolt when: goal achieved, all items done, 1 week elapsed, or theme shifted
- Archive completed Bolts in `docs/pm/SPRINT-LOG.md` with metrics and retro

## The Five Questions (Before Starting Work)

Before each session, answer:

1. **What's the goal?** — Single sentence describing the outcome
2. **What's in scope?** — Specific items to work on
3. **What's out of scope?** — Things explicitly not being done
4. **What's blocked?** — External dependencies or unknowns
5. **What's the exit criteria?** — How do you know you're done?

## Context Hygiene

- `CLAUDE.md` is the AI operating manual — keep it current
- `docs/pm/CURRENT-SPRINT.md` is the live dashboard
- Commit frequently with descriptive messages
- Update PM docs at session start and end
- Use `/pm` to run PM review at checkpoints

## Quality Gates (Every Commit)

Pre-commit hooks enforce:
1. **Black** — Code formatted (line-length 100)
2. **Pylint** — Lint score 10/10
3. **Pytest** — Unit tests pass

## Quality Gates (Every Bolt)

Before closing a Bolt:
1. All tests pass (`make test`)
2. Pylint 10/10 (`make lint`)
3. CLAUDE.md updated with current metrics
4. CHANGELOG.md updated with changes
5. Sprint archived with retro

## AI-Pair Patterns

- **Plan first:** Use plan mode for non-trivial features
- **Read before edit:** Always read existing code before modifying
- **Test alongside:** Write tests as features are built, not after
- **Commit atomically:** One logical change per commit
- **Memory over context:** Use `/pm`, CLAUDE.md, and memory tools to persist knowledge across sessions
