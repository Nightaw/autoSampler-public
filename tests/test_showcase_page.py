from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_showcase_page import build_html


class ShowcasePageTest(unittest.TestCase):
    def test_build_html_contains_key_sections(self) -> None:
        html = build_html()
        self.assertIn("autoSampler Public Showcase", html)
        self.assertIn("Post-capture sampling turned into a portfolio-grade service demo.", html)
        self.assertIn("GET /demo/showcase", html)
        self.assertIn("../samples/results/stall_storyboard.jpg", html)
        self.assertIn("../docs/generated/scenario-comparison.svg", html)
        self.assertIn("../docs/interview-brief.md", html)



if __name__ == "__main__":
    unittest.main()
