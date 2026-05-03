# Human/AI Bio-Acceleration Research

Static research archive on physiology, cognition, rituals, diet, fermentation, and adaptive systems.

This repository is a public HTML archive, not a protocol engine and not medical advice. The standard is evidence first: claims should be traceable to sources, uncertainty should stay visible, and reports that touch health or cognition need stronger publication hygiene than ordinary essays.

## Current shape

- `index.html` is the research hub.
- `*-report.html` files are standalone long-form reports.
- `.github/workflows/security-audit.yml` scans for secrets and SAST issues.
- `.github/workflows/quality.yml` runs the local quality gate and static build check.

## Quality gate

Run:

```bash
npm test
```

This executes:

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_reports.py
```

The audit checks every HTML report for:

- page title and H1
- meta description
- canonical URL
- Open Graph metadata
- Twitter card metadata
- external source links on report pages
- numeric claims without source links
- source/reference language without links
- medical-advice disclaimer
- broken internal `.html` links

## Baseline policy

The current archive has legacy publication-hygiene debt. It is recorded in:

```text
tools/audit_baseline.json
```

CI allows accepted legacy issues but blocks new unbaselined issues.

To see the full debt:

```bash
python3 tools/audit_reports.py --strict
```

To inspect machine-readable output:

```bash
python3 tools/audit_reports.py --strict --json
```

Do not update the baseline casually. Updating it means accepting new debt.

## Deploy

This is a static site.

Vercel settings:

- Framework Preset: `Other`
- Build Command: `npm run build`
- Output Directory: `.`
- Install Command: `npm install`

The build command is intentionally a no-op because the archive is committed as static HTML.

## Publication standard

Before adding or promoting a report:

1. Add concrete external sources for factual and numeric claims.
2. Include a clear `Not medical advice` disclaimer when the topic touches health, cognition, hormones, sleep, diet, supplementation, or protocols.
3. Add social/share metadata so the report does not render as an anonymous HTML file.
4. Run `npm test`.
5. If the audit fails, fix the page. Do not add the failure to the baseline unless the debt is intentionally accepted.

## Not medical advice

The content in this repository is for research and educational purposes only. It is not medical advice, diagnosis, treatment, or a substitute for professional healthcare guidance.
