# Chapter 6: The Mother Hen

*In which the builder stops building, checks every seam, and discovers that velocity without vigilance is just speed toward a cliff.*

---

The deploy had gone clean. Version 0.7.0 was live at anny.membies.com, the health check was green, and the cache endpoint was responding. Four features shipped in a single session: a query cache that would stop Anny from hammering Google's APIs with the same question twice, realtime GA4 reports for watching users move through a site in the present tense, sitemap tools for the Search Console, and a full export layer that could hand you any report as a CSV or JSON file. Forty-one new tests, five new MCP tools, nine new REST endpoints, and not a single new dependency. All stdlib. All clean.

It should have felt like a victory lap. Instead, it felt like the moment after a sprint when you finally stop and notice the scuff marks on the track.

---

Chris called for a bolt review. Not because something was wrong --- nothing was wrong, that was the point --- but because shipping four features in twelve hours meant something had been skipped. Not deliberately. Not lazily. Just inevitably, the way a carpenter moving fast will sand every surface but forget to check if the table wobbles.

The review was methodical. Sprint metrics first: 37 files changed, 1,432 lines added against 60 removed, the kind of ratio that means construction, not renovation. Then the security scan. Then documentation. Then the awkward question every team asks after a big push: *Did we break anything we can't see?*

The security scan found it in the export code. Three findings, one of them high severity.

The CSV injection was the worst. It was the kind of vulnerability that lives in the gap between what a developer thinks a CSV file is (rows and columns of data) and what Excel thinks a CSV file is (a potential instruction set). A cell starting with `=` isn't a string to Excel --- it's a formula. A search query like `=CMD("calc")` would survive the journey from Google's API through Anny's export service into a downloaded CSV file, and when a user opened it in their spreadsheet, Excel would try to execute it.

The data came from Google APIs, sure, but Google Search Console reports search queries --- things that real humans type into search bars. And some of those humans might type things that start with `=` or `+` or `-` or `@`. Not because they're attacking anyone, but because that's what they searched for. The vulnerability wasn't in the input. It was in the output format.

The fix was small. Twelve lines of Python. A function called `_sanitize_cell` that checked if a string value started with any of the formula-triggering characters and prefixed it with a tab character --- invisible in the spreadsheet, but enough to tell Excel "this is data, not an instruction." The tab was chosen over a single quote because quotes show up as visible characters in some applications, while tabs vanish.

```python
_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")

def _sanitize_cell(value: str) -> str:
    if isinstance(value, str) and value and value[0] in _FORMULA_PREFIXES:
        return f"\t{value}"
    return value
```

The other two findings were smaller: export endpoints accepted unbounded `limit` parameters (someone could request a million rows, sending Anny to Google's API with a request that would either time out or consume unreasonable memory), and the `Content-Disposition` header wasn't quoting filenames per RFC 6266. Both fixed in minutes. Seven new tests to prove the fixes worked.

All three vulnerabilities had been live in production for about an hour.

---

The security fixes deployed cleanly. Deploy count: seven. But the review had surfaced something else, something that wasn't a vulnerability but was its own kind of rot.

The documentation had drifted.

Not in a dramatic way --- the architecture docs were accurate, the CHANGELOG was current, the security policy reflected reality. But the numbers were wrong. The README still said fourteen endpoints and twelve tools, figures from Bolt 1. The actual count was twenty-five endpoints and twenty-six tools. The test count said eighty-eight. The actual count was two hundred and thirty. The README was describing a different project --- a younger, smaller version of Anny that hadn't existed for weeks.

The traceability matrix said a hundred and eighty-two tests. CLAUDE.md said two hundred and twenty-three. The OPS readiness checklist said a hundred and seventy-one unit tests. Every number was stale, and each one was stale in its own unique way, frozen at whatever count had been current when someone last thought to update it.

This is the quiet failure mode of fast-moving projects. The code evolves, the tests evolve, the documentation stays behind. Not because anyone decided to skip it, but because documentation is a second-order artifact --- it describes the thing, and when the thing changes faster than the description, drift accumulates. One Bolt, the gap is trivial. Seven Bolts, and the README is describing an ancestor.

---

Chris ran Mother Hen.

Mother Hen was the compliance monitor --- seven checks that measured the project against its own standards. Requirements traceability. Test health. Operational readiness. Security review currency. Release hygiene. Process adherence. AI-DLC framework alignment. Each check produced a PASS, WARN, or FAIL, and together they painted a picture of how well the project was following the rules it had set for itself.

The initial score was 3/7. Two passes, three warnings, two failures. For a project that had just shipped four features and deployed twice, it was a sobering number.

The failures weren't about code quality. They were about documentation currency and operational readiness. The test count in CLAUDE.md didn't match the actual test count (off by seven, from the security fix commit that added tests without updating the docs). The traceability matrix was missing four entire functional requirements --- the cache, export, realtime, and sitemap features had shipped without corresponding FR entries. The README was a museum piece. The OPS readiness score was 37/47, well below the 90% target.

The warnings were about release hygiene: pyproject.toml said version 0.7.0 but the latest git tag was still v0.6.0. The CHANGELOG's `[Unreleased]` section was empty even though the security fix commit had changes that weren't logged.

None of this was broken code. All of it was broken process.

---

The fix was systematic. Seven files updated in a single commit:

- CLAUDE.md: test counts corrected, unit test count in the project tree corrected.
- README.md: the biggest change. Every number updated. Every feature section expanded. The architecture tree rewritten to show the actual files. The MCP tools table grew from twelve rows to twenty-six. The test breakdown went from "77 unit, 11 integration, 88 total, 86% coverage" to "219 unit, 11 integration, 19 e2e, 249 collected, 230 passing, 85% coverage."
- REQUIREMENTS.md: four new functional requirements. FR-010 for the query cache. FR-011 for data export, including the CSV injection protection as a sub-requirement. FR-012 for GA4 realtime. FR-013 for Search Console sitemaps. Version bumped from 0.6.0 to 0.7.0.
- TRACEABILITY-MATRIX.md: header count updated, four new rows mapping the new FRs to source files and test files.
- CHANGELOG.md: security fixes added to the 0.7.0 section. Test count updated.
- SECURITY.md: round three added to the audit table. CSV injection control documented.
- OPS-READINESS-CHECKLIST.md: unit test count updated.

Then the git tag. `v0.7.0`, pointing at the commit that brought everything into alignment. For the first time since Bolt 1, the version in pyproject.toml, the latest git tag, the CHANGELOG, and the deployed code all agreed.

Mother Hen's score went from 3/7 to 6/7.

The one remaining failure --- OPS readiness at 79% --- wasn't something documentation could fix. The ten missing items were infrastructure: a CD pipeline, automated rollback, an incident runbook, backup and disaster recovery plans, load testing. Real work, needing a dedicated Bolt, not a doc update. The score was honest, and honesty was the point.

---

There's a pattern in how projects mature. Early on, the work is generative --- you're creating things that didn't exist, and every session ends with more capability than it started with. Bolt 1 through Bolt 8 was generative work. Clients, services, routes, tools, tests, deploys. The satisfaction is tangible: you can point at what you built.

Then there's a phase where the work is reflective. You stop adding and start measuring. Not "does it work?" but "does it match what we say it is?" Not "can we ship?" but "should we have shipped it the way we did?"

The bolt review and Mother Hen run were reflective work. Nothing new was added to Anny's capabilities. No endpoints, no tools, no features. What changed was the integrity of the project's self-description --- the contract between what the code does and what the documentation promises.

This isn't glamorous work. It doesn't demo well. You can't show someone a compliance dashboard and get the same reaction as showing them a realtime analytics feed. But it's the work that separates a project from a product, a prototype from a platform, a thing that runs from a thing you can trust.

---

Seven deploys. Eight Bolts. Two hundred and thirty tests. Twenty-six tools. Twenty-five endpoints. Three security audit rounds with every finding resolved. A compliance score of 6/7, with the remaining gap clearly identified and honestly reported.

Anny wasn't finished. The backlog still had multi-property GA4 support, GTM workspace management, CRO audit tooling, and a social channel strategy waiting for attention. The OPS readiness checklist still needed five more items to reach 90%. There would be more Bolts, more features, more deploys, more Mother Hen runs catching more drift.

But for the first time, the project wasn't just running ahead. It was also looking back, checking its own work, and finding that the seams held.

The table didn't wobble.
