from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from common.job_queue import reset_jobs


class WorkerApiTest(unittest.TestCase):
    def setUp(self) -> None:
        reset_jobs()
        self.client = create_app().test_client()

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "ok")

    def test_scenarios(self) -> None:
        response = self.client.get("/demo/scenarios")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["scenarios"][0]["name"], "baseline_prescreen")

    def test_scenario_detail(self) -> None:
        response = self.client.get("/demo/scenarios/resolution_consistency_review")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["execution_profile"], "resolution_audit")

    def test_devices(self) -> None:
        response = self.client.get("/demo/devices?platform=android")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(all(device["platform"] == "android" for device in data["devices"]))

    def test_run_demo(self) -> None:
        response = self.client.post("/demo/run", json={"scenario": "baseline_prescreen"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["summary"]["final_decision"], "pass")
        self.assertEqual(data["summary"]["stall_count"], 2)

    def test_markdown_report(self) -> None:
        response = self.client.get("/demo/report.md?scenario=baseline_prescreen")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("# Baseline Label Prescreen", body)

    def test_architecture(self) -> None:
        response = self.client.get("/demo/architecture")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(data["scenario_count"], 2)

    def test_showcase(self) -> None:
        response = self.client.get("/demo/showcase")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["project"], "autoSampler Public")

    def test_job_lifecycle(self) -> None:
        created = self.client.post("/demo/jobs", json={"scenario": "baseline_prescreen"})
        self.assertEqual(created.status_code, 201)
        job = created.get_json()
        self.assertEqual(job["status"], "queued")

        listed = self.client.get("/demo/jobs")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.get_json()["jobs"]), 1)

        processed = self.client.post("/demo/jobs/process")
        self.assertEqual(processed.status_code, 200)
        processed_job = processed.get_json()
        self.assertEqual(processed_job["status"], "finished")
        self.assertEqual(processed_job["report"]["summary"]["final_decision"], "pass")

        detail = self.client.get(f"/demo/jobs/{processed_job['job_id']}")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.get_json()["status"], "finished")


if __name__ == "__main__":
    unittest.main()
