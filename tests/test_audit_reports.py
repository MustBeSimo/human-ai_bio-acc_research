import json
import tempfile
import unittest
from pathlib import Path

from tools.audit_reports import audit, write_baseline


GOOD_REPORT = """<!doctype html>
<html lang="en"><head>
<title>Good report</title>
<meta name="description" content="Evidence-backed research note.">
<meta property="og:title" content="Good report">
<meta property="og:description" content="Evidence-backed research note.">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://example.com/good-report.html">
</head><body>
<h1>Good report</h1>
<p>This is educational, not medical advice.</p>
<p>Claim: 10% change in a measured outcome.</p>
<a href="https://pubmed.ncbi.nlm.nih.gov/123/">source</a>
</body></html>"""

BAD_REPORT = """<!doctype html>
<html lang="en"><head><title>Bad</title></head><body>
<h1>Bad</h1><p>50% increase in something.</p>
</body></html>"""


class AuditReportsTest(unittest.TestCase):
    def test_good_report_has_no_new_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tools").mkdir()
            (root / "good-report.html").write_text(GOOD_REPORT, encoding="utf-8")
            issues, new = audit(root, baseline=set())
            self.assertEqual(issues, [])
            self.assertEqual(new, [])

    def test_bad_report_fails_without_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tools").mkdir()
            (root / "bad-report.html").write_text(BAD_REPORT, encoding="utf-8")
            issues, new = audit(root, baseline=set())
            codes = {issue.code for issue in new}
            self.assertIn("missing_meta_description", codes)
            self.assertIn("missing_external_sources", codes)
            self.assertIn("numeric_claims_without_links", codes)
            self.assertIn("missing_medical_disclaimer", codes)

    def test_baseline_allows_legacy_issues_but_strict_still_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tools").mkdir()
            (root / "bad-report.html").write_text(BAD_REPORT, encoding="utf-8")
            write_baseline(root)
            baseline = set(json.loads((root / "tools" / "audit_baseline.json").read_text())["accepted_issues"])
            _, new = audit(root, baseline=baseline)
            strict_issues, strict_new = audit(root, strict=True)
            self.assertEqual(new, [])
            self.assertGreater(len(strict_issues), 0)
            self.assertEqual(len(strict_issues), len(strict_new))


if __name__ == "__main__":
    unittest.main()
