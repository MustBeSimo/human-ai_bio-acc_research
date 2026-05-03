import json
import unittest
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent


class ProjectMetadataTest(unittest.TestCase):
    def test_vercel_static_build_config_exists(self):
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertEqual(config["buildCommand"], "npm run build")
        self.assertEqual(config["outputDirectory"], ".")
        self.assertEqual(config["installCommand"], "npm install")

    def test_package_scripts_run_quality_gate(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertIn("python3 tools/audit_reports.py", package["scripts"]["test"])
        self.assertIn("static archive", package["scripts"]["build"])

    def test_sitemap_contains_every_html_report_except_404(self):
        tree = ElementTree.parse(ROOT / "sitemap.xml")
        urls = {node.text for node in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
        html_files = {p.name for p in ROOT.glob("*.html") if p.name != "404.html"}
        for name in html_files:
            self.assertTrue(any(url.endswith(f"/{name}") for url in urls), name)

    def test_robots_points_to_sitemap(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap:", robots)


if __name__ == "__main__":
    unittest.main()
