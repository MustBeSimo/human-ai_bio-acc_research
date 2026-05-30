import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


class IndexEditorialAtlasV2Test(unittest.TestCase):
    def setUp(self):
        self.html = INDEX.read_text(encoding="utf-8")

    def test_pale_blue_tonal_system_exists(self):
        for token in [
            "--blue: #dbeafe",
            "--blue-strong: #9bb7d4",
            "--blue-ink: #35536f",
            "--mist: #edf5fb",
        ]:
            self.assertIn(token, self.html)

    def test_sophisticated_editorial_regions_exist(self):
        for marker in [
            'class="atlas-canvas"',
            'class="editorial-spine"',
            'class="folio-strip"',
            'class="specimen-panel"',
            'class="research-ledger"',
            'class="annotation-stack"',
        ]:
            self.assertIn(marker, self.html)

    def test_hero_has_layered_editorial_composition(self):
        for copy in [
            "Field notes for adaptive systems",
            "A calmer index for biology, cognition, and cultural protocols",
            "Evidence, source hygiene, and reading order are treated as interface objects",
            "Atlas plate 01",
        ]:
            self.assertIn(copy, self.html)

    def test_existing_cards_are_preserved(self):
        self.assertEqual(self.html.count('class="research-card"'), 14)
        for title in [
            "Breath as Operating System",
            "Fermentation Rituals as Adaptive Protocols",
            "Music Is Not Taste. It Is Telemetry.",
            "AI × Testosterone: Unlocking Peak Performance",
        ]:
            self.assertIn(title, self.html)


if __name__ == "__main__":
    unittest.main()
