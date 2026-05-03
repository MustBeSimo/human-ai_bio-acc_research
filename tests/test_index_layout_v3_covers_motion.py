from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class LayoutV3CoversMotionTests(unittest.TestCase):
    def test_substack_cover_images_populate_cards(self):
        self.assertGreaterEqual(HTML.count('class="card-cover-image"'), 12)
        self.assertGreaterEqual(HTML.count('https://substackcdn.com/image/fetch/'), 12)
        self.assertIn('data-cover-source="substack-og-image"', HTML)
        self.assertIn('loading="lazy"', HTML)
        self.assertIn('decoding="async"', HTML)

    def test_layout_is_not_plain_uniform_grid(self):
        self.assertIn('class="cover-marquee"', HTML)
        self.assertIn('data-featured="true"', HTML)
        self.assertIn('.research-card[data-featured="true"]', HTML)
        self.assertIn('grid-column: span 2', HTML)
        self.assertIn('class="card-body"', HTML)
        self.assertIn('class="card-number"', HTML)

    def test_parallax_motion_exists_with_accessibility_fallback(self):
        self.assertIn('data-parallax', HTML)
        self.assertIn('requestAnimationFrame', HTML)
        self.assertIn('prefers-reduced-motion: reduce', HTML)
        self.assertIn('matchMedia("(prefers-reduced-motion: reduce)")', HTML)

    def test_readability_constraints_are_explicit(self):
        self.assertRegex(HTML, r'\.research-card p \{[^}]*line-height: 1\.7')
        self.assertIn('text-wrap: pretty', HTML)
        self.assertIn('max-width: 62ch', HTML)
        self.assertIn('font-size: clamp(1rem, 1.08vw, 1.08rem)', HTML)


if __name__ == "__main__":
    unittest.main()
