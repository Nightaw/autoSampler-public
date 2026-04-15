from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_site_bundle import build_case_page, markdown_to_html, rewrite_showcase_for_site
from tools.build_showcase_page import build_html


class SiteBundleTest(unittest.TestCase):
    def test_rewrite_showcase_for_site_repoints_assets(self) -> None:
        html = rewrite_showcase_for_site(build_html())
        self.assertIn("./assets/results/stall_storyboard.jpg", html)
        self.assertIn("./interview-brief.html", html)
        self.assertIn("./data/showcase_manifest.json", html)

    def test_markdown_to_html_wraps_content(self) -> None:
        html = markdown_to_html("# Title\n\n- one\n- two\n", "Title")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<li>one</li>", html)

    def test_case_page_contains_summary(self) -> None:
        html = build_case_page(
            "baseline_prescreen.json",
            stylesheet_href="../showcase.css",
            back_href="../index.html",
            storyboard_href="../assets/results/stall_storyboard.jpg",
            timeline_href="../assets/generated/baseline-timeline.svg",
        )
        self.assertIn("Baseline Label Prescreen", html)
        self.assertIn("Execution trace", html)


if __name__ == "__main__":
    unittest.main()
