import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


class IndexEditorialAtlasRestyleTest(unittest.TestCase):
    def setUp(self):
        self.html = INDEX.read_text(encoding="utf-8")

    def test_sage_editorial_atlas_design_tokens_exist(self):
        required_tokens = {
            "--bg: #f6f3ea",
            "--surface: #fffdf8",
            "--surface-2: #eef3e9",
            "--paper: #fbf8ef",
            "--border: #d8ddcf",
            "--border-strong: #b9c4ad",
            "--text: #151713",
            "--muted: #6d7467",
            "--sage: #8fa58a",
        }
        for token in required_tokens:
            self.assertIn(token, self.html)

    def test_index_uses_editorial_atlas_shell(self):
        for marker in [
            "Bio/Acc Atlas · Sage edition",
            "class=\"atlas-canvas\"",
            "class=\"editorial-spine\"",
            "Field notes for adaptive systems",
            "Research is the interface",
        ]:
            self.assertIn(marker, self.html)

    def test_all_existing_report_cards_survive_restyle(self):
        cards = re.findall(r'class="research-card"', self.html)
        self.assertEqual(len(cards), 14)
        for report in [
            "breath-os-report.html",
            "fermentation-rituals-full-report.html",
            "music-telemetry-report.html",
            "ai-testosterone-report.html",
            "sunrise-os-report.html",
            "mediterranean-diet-report.html",
        ]:
            self.assertIn(report, self.html)


if __name__ == "__main__":
    unittest.main()
