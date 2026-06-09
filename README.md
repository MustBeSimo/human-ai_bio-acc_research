# Human / AI Bio-Acceleration Research

A field notebook on the systems that run a body, a mind, and a self
under continuous machine observation.

Fourteen reports. Six tracks. One thesis: the levers that actually move
the organism — light, breath, cold, food, rhythm, hormone, story — are
older than the technology now measuring them. The interesting question
is no longer *what to do* but *what an AI infers about you when you do
it*.

- **Live archive** → https://mustbesimo.github.io/human-ai_bio-acc_research/
- **Companion essays (Substack)** → https://simoleonelli.substack.com/
- **Source** → https://github.com/MustBeSimo/human-ai_bio-acc_research

---

## What this is

This is not a newsletter, not a protocol shop, not medical advice. It
is a long-form public archive that holds itself accountable to
peer-reviewed literature: numeric claims sit next to their sources, every
health-adjacent page carries an explicit disclaimer, and an auditor
runs in CI before anything ships.

The voice is opinionated; the citations are not.

---

## The atlas

`index.html` is the entry point — an editorial atlas of cards in
reverse-chronological order, each routing to its full report and, when
published, its companion Substack essay.

The fourteen reports cluster into six tracks:

### 1 — Autonomic engineering · the levers you drive directly

- **`breath-os-report.html`** · *Breath as Operating System.* CO₂
  tolerance, vagal tone, and the pre-Bötzinger → locus coeruleus arousal
  circuit. Three knobs — rate, ratio, CO₂ load — and five named
  protocols mapped to them.
- **`sunrise-os-report.html`** · *Sunrise as Operating System.* The
  cortisol awakening response as a launch sequence; light, cold,
  movement, breath as the first hour's six phases.

### 2 — Brain & sleep architecture

- **`brain-waves-101-report.html`** · Delta, theta, alpha, beta, gamma
  as functional bands with daily cycles and practical levers.
- **`delta-engineering-report.html`** · Designing the night to train
  tomorrow's brain. Slow-wave sleep as a compilation step.
- **`rewire-brain-report.html`** · A fourteen-step neuroplasticity
  playbook — screen-fog to strength.

### 3 — Chronobiology

- **`seasonal-cognition-report.html`** · Four neurochemical firmware
  versions a year. Spring / dopamine, summer / serotonin, autumn /
  acetylcholine, winter / melatonin.

### 4 — Hormonal & bioelectric

- **`ai-testosterone-report.html`** · AI-assisted hormonal
  optimization without the bro-science.
- **`bioelectric-rituals-report.html`** · Cortisol, dopamine,
  acetylcholine, and the ancient timing that anticipated them.

### 5 — Edible biotech

- **`fermentation-rituals-full-report.html`** · Twelve cross-cultural
  cases of fermentation as a socially governed, microbially executed
  adaptive protocol.
- **`gut-biohack-report.html`** · AI-guided microbes for gut, mood,
  and metabolic health.
- **`evoo-report.html`** · Extra virgin olive oil as a pharmacological
  agent. Six bioactive compounds, mapped.
- **`mediterranean-diet-report.html`** · Sixty years of peer review,
  distilled into one field guide.

### 6 — Adaptive systems & the AI mirror

- **`attunement-report.html`** · From optimization to attunement —
  cycles as a design principle rather than a metric to suppress.
- **`music-telemetry-report.html`** · What an AI infers about you
  from the cultural surface of your taste. Identity compression as
  the architecture of capture.

---

## Publication standard

The reports are written to a stricter bar than the genre default:

1. External, primary-literature links sit next to numeric claims.
2. Every health-adjacent report carries an explicit
   *Not medical advice* disclaimer.
3. Social and share metadata — canonical link, Open Graph, Twitter card
   — is required, not optional.
4. A deterministic, stdlib-only auditor runs in CI and blocks new
   publication-hygiene debt.

Legacy debt from the original drop is recorded in
`tools/audit_baseline.json` and is paid down report-by-report rather
than papered over. New reports must pass strict mode from day one.

## Quality gate

```bash
npm test
```

Runs the unit tests and the auditor in one pass:

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_reports.py
```

The audit checks every HTML report for:

- `<title>` and `<h1>`
- meta description
- canonical URL
- Open Graph metadata
- Twitter card metadata
- external source links on report pages
- numeric claims without source links
- source / reference language without links
- medical-advice disclaimer
- broken internal `.html` links

CI accepts grandfathered issues from `audit_baseline.json` and blocks
anything new.

To see the full debt at any time:

```bash
python3 tools/audit_reports.py --strict
```

Machine-readable output:

```bash
python3 tools/audit_reports.py --strict --json
```

Do not update the baseline casually. Updating it means accepting new
debt.

## Repository shape

```
.
├── index.html                       — the atlas
├── *-report.html                    — standalone long-form reports
├── tools/audit_reports.py           — publication-hygiene auditor
├── tools/audit_baseline.json        — accepted legacy debt
├── tests/                           — unit tests: layout, metadata, audit
├── sitemap.xml, robots.txt          — discovery surface
├── vercel.json, package.json        — static deploy config
└── .github/workflows/               — quality gate + scheduled security audit
```

## Deploy

Two hosts, one tree:

- **GitHub Pages** (canonical):
  <https://mustbesimo.github.io/human-ai_bio-acc_research/>
- **Vercel** (static):
  - Framework Preset: `Other`
  - Build Command: `npm run build` *(intentional no-op)*
  - Output Directory: `.`
  - Install Command: `npm install`

The archive is committed as static HTML; there is nothing to compile.

## Adding a report

1. Add concrete external sources for factual and numeric claims.
2. Include a clear *Not medical advice* disclaimer when the topic
   touches health, cognition, hormones, sleep, diet, supplementation,
   or protocols.
3. Add canonical / Open Graph / Twitter card metadata.
4. Run `npm test`.
5. If the audit fails, fix the page — do not add the failure to the
   baseline unless the debt is intentionally accepted.

## Author

**Simone Leonelli** — independent writer and researcher working at the
overlap of biology, fermentation, microbiology, adaptive systems, and
the machine intelligence that is now reading all of it back to us.

Companion essays: <https://simoleonelli.substack.com/>

## Not medical advice

The content in this repository is for research and educational purposes
only. It is not medical advice, diagnosis, treatment, or a substitute
for professional healthcare guidance.
