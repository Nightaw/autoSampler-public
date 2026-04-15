from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_interview_brief import build_markdown
from tools.build_visual_assets import build_architecture_export, build_device_matrix, build_scenario_comparison, build_timeline


class VisualAssetsTest(unittest.TestCase):
    def test_svg_builders_emit_expected_titles(self) -> None:
        self.assertIn("autoSampler public flow", build_architecture_export())
        self.assertIn("scenario comparison", build_scenario_comparison())
        self.assertIn("device capability matrix", build_device_matrix())
        self.assertIn("baseline timeline", build_timeline("baseline_prescreen.json", "baseline timeline"))

    def test_interview_brief_contains_summary(self) -> None:
        markdown = build_markdown()
        self.assertIn("# Interview Brief", markdown)
        self.assertIn("30-Second Summary", markdown)
        self.assertIn("resolution_consistency_review", markdown)


if __name__ == "__main__":
    unittest.main()

