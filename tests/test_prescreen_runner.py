from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import build_markdown_report, describe_architecture, list_scenarios, run_demo_scenario


class PrescreenRunnerTest(unittest.TestCase):
    def test_list_scenarios(self) -> None:
        scenarios = list_scenarios()
        self.assertEqual(scenarios[0]["name"], "baseline_prescreen")
        self.assertEqual(len(scenarios), 2)

    def test_run_demo_scenario(self) -> None:
        report = run_demo_scenario("baseline_prescreen")
        self.assertEqual(report["summary"]["unit_id"], "20260324190033")
        self.assertEqual(report["summary"]["final_decision"], "pass")
        self.assertEqual(report["summary"]["stall_count"], 2)
        self.assertEqual(report["summary"]["resolution_count"], 3)
        self.assertEqual(report["execution"]["status"], "passed")

    def test_markdown_report(self) -> None:
        report = build_markdown_report("baseline_prescreen")
        self.assertIn("# Baseline Label Prescreen", report)
        self.assertIn("Final decision: pass", report)

    def test_architecture_summary(self) -> None:
        architecture = describe_architecture()
        self.assertGreaterEqual(architecture["scenario_count"], 2)
        self.assertIn("flask demo api", architecture["pipeline_layers"])


if __name__ == "__main__":
    unittest.main()

