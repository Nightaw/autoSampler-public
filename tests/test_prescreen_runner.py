from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.device_registry import list_devices
from common.prescreen_runner import build_markdown_report, build_showcase_manifest, describe_architecture, list_scenarios, run_demo_scenario


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
        self.assertEqual(report["devices"][0]["role"], "capture")
        self.assertEqual(report["execution"]["profile"], "prescreen")

    def test_secondary_scenario(self) -> None:
        report = run_demo_scenario("resolution_consistency_review")
        self.assertEqual(report["summary"]["unit_id"], "20260324195510")
        self.assertEqual(report["summary"]["final_decision"], "review")
        self.assertGreaterEqual(len(report["metrics"]["heuristic"]["warnings"]), 1)

    def test_markdown_report(self) -> None:
        report = build_markdown_report("baseline_prescreen")
        self.assertIn("# Baseline Label Prescreen", report)
        self.assertIn("Final decision: pass", report)
        self.assertIn("## Devices", report)

    def test_architecture_summary(self) -> None:
        architecture = describe_architecture()
        self.assertGreaterEqual(architecture["scenario_count"], 2)
        self.assertIn("flask demo api", architecture["pipeline_layers"])
        self.assertGreaterEqual(len(architecture["available_devices"]), 3)

    def test_device_registry(self) -> None:
        devices = list_devices(platform="ios")
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["device_id"], "ios-lab-01")

    def test_showcase_manifest(self) -> None:
        manifest = build_showcase_manifest()
        self.assertEqual(manifest["project"], "autoSampler Public")
        self.assertEqual(len(manifest["scenarios"]), 2)


if __name__ == "__main__":
    unittest.main()
