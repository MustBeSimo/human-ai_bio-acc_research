#!/usr/bin/env python3
"""Audit static Bio/Acc research reports for publication hygiene.

The audit is deterministic and stdlib-only. Existing debt can be recorded in
`tools/audit_baseline.json` so CI blocks new regressions without pretending the
current archive is cleaner than it is.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "tools" / "audit_baseline.json"
EXTERNAL_RE = re.compile(r"^https?://", re.I)
NUMERIC_CLAIM_RE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:%|mg|g|kg|Hz|bpm|minutes?|hours?|days?|weeks?|months?|years?)",
    re.I,
)
SOURCE_HINT_RE = re.compile(
    r"\b(?:source|sources|references|bibliography|doi|pubmed|ncbi|nih|study|trial|review|meta-analysis|fao|who|unesco|nature|science)\b",
    re.I,
)
DISCLAIMER_RE = re.compile(r"not\s+(?:medical|health)\s+advice|educational\s+purposes", re.I)
SKIP_FILES = {"404.html"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.h1 = ""
        self.meta: dict[tuple[str, str], str] = {}
        self.links: list[str] = []
        self._capture: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k.lower(): (v or "") for k, v in attrs_list}
        tag = tag.lower()
        if tag in {"title", "h1"}:
            self._capture = tag
            self._buf = []
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            content = attrs.get("content", "").strip()
            if key:
                self.meta[("meta", key.lower())] = content
        if tag == "link":
            rel = attrs.get("rel", "").lower()
            href = attrs.get("href", "").strip()
            if rel and href:
                self.meta[("link", rel)] = href
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"].strip())

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._capture == tag:
            text = re.sub(r"\s+", " ", " ".join(self._buf)).strip()
            if tag == "title":
                self.title = text
            elif tag == "h1":
                self.h1 = text
            self._capture = None
            self._buf = []


@dataclass(frozen=True)
class Issue:
    file: str
    code: str
    message: str

    def key(self) -> str:
        return f"{self.file}:{self.code}"


def report_files(root: Path) -> list[Path]:
    return sorted(p for p in root.glob("*.html") if p.name not in SKIP_FILES)


def parse_page(path: Path) -> tuple[PageParser, str]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    parser = PageParser()
    parser.feed(html)
    return parser, html


def audit_file(path: Path, root: Path) -> list[Issue]:
    parser, html = parse_page(path)
    rel = path.relative_to(root).as_posix()
    issues: list[Issue] = []

    def issue(code: str, message: str) -> None:
        issues.append(Issue(rel, code, message))

    if not parser.title:
        issue("missing_title", "Missing <title>.")
    if not parser.h1:
        issue("missing_h1", "Missing <h1>.")
    if not parser.meta.get(("meta", "description")):
        issue("missing_meta_description", "Missing meta description.")
    if not parser.meta.get(("link", "canonical")):
        issue("missing_canonical", "Missing canonical link.")
    if not parser.meta.get(("meta", "og:title")):
        issue("missing_og_title", "Missing og:title.")
    if not parser.meta.get(("meta", "og:description")):
        issue("missing_og_description", "Missing og:description.")
    if not parser.meta.get(("meta", "twitter:card")):
        issue("missing_twitter_card", "Missing twitter:card.")

    external_links = [href for href in parser.links if EXTERNAL_RE.search(href)]
    if path.name != "index.html":
        if not external_links:
            issue("missing_external_sources", "Report has no external source links.")
        if NUMERIC_CLAIM_RE.search(html) and not external_links:
            issue("numeric_claims_without_links", "Numeric claims exist but no external source links are present.")
        if SOURCE_HINT_RE.search(html) and not external_links:
            issue("source_terms_without_links", "Source/reference language appears but no external source links are present.")
        if not DISCLAIMER_RE.search(html):
            issue("missing_medical_disclaimer", "Health/cognition report needs a not-medical-advice disclaimer.")

    for href in [x for x in parser.links if x.endswith(".html") and not EXTERNAL_RE.search(x)]:
        target_name = href.split("#", 1)[0]
        if not (path.parent / target_name).exists():
            issue("broken_internal_link", f"Broken internal link: {href}")

    return issues


def load_baseline(path: Path = BASELINE_PATH) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("accepted_issues", []))


def audit(root: Path = ROOT, *, baseline: set[str] | None = None, strict: bool = False) -> tuple[list[Issue], list[Issue]]:
    issues = [issue for path in report_files(root) for issue in audit_file(path, root)]
    allowed = set() if strict else (baseline if baseline is not None else load_baseline(root / "tools" / "audit_baseline.json"))
    new_issues = [issue for issue in issues if issue.key() not in allowed]
    return issues, new_issues


def write_baseline(root: Path = ROOT, path: Path | None = None) -> None:
    issues, _ = audit(root, baseline=set(), strict=True)
    target = path or root / "tools" / "audit_baseline.json"
    payload = {
        "note": "Accepted legacy publication-hygiene debt. CI fails on new issues. Run `python tools/audit_reports.py --strict` to see full debt.",
        "accepted_issues": sorted(issue.key() for issue in issues),
    }
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit static research reports.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true", help="Fail on every issue, ignoring baseline.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--write-baseline", action="store_true", help="Rewrite tools/audit_baseline.json from current issues.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.write_baseline:
        write_baseline(args.root)

    issues, new_issues = audit(args.root, strict=args.strict)
    if args.json:
        print(json.dumps({
            "total_issues": len(issues),
            "new_issues": len(new_issues),
            "issues": [issue.__dict__ for issue in issues],
            "new": [issue.__dict__ for issue in new_issues],
        }, indent=2, sort_keys=True))
    else:
        print(f"Reports audited: {len(report_files(args.root))}")
        print(f"Total issues: {len(issues)}")
        print(f"New issues: {len(new_issues)}")
        for issue in new_issues[:80]:
            print(f"{issue.key()} - {issue.message}")
        if len(new_issues) > 80:
            print(f"... {len(new_issues) - 80} more")
    return 1 if new_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
