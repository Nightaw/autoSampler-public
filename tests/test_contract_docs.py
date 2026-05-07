from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import (
    build_agent_ecosystem_manifest,
    build_agent_handoff_manifest,
    build_artifact_schema,
    build_scenario_template_manifest,
)
from tools.build_agent_docs import build_markdown as build_agent_markdown


class ContractDocsTest(unittest.TestCase):
    def test_template_manifest(self) -> None:
        manifest = build_scenario_template_manifest()
        self.assertEqual(manifest["project"], "autoSampler Public")
        self.assertGreaterEqual(len(manifest["templates"]), 3)

    def test_artifact_schema_shape(self) -> None:
        schema = build_artifact_schema()
        self.assertEqual(schema["title"], "autoSampler Public Artifact Manifest")
        self.assertIn("artifact_groups", schema["properties"])

    def test_agent_ecosystem_manifest(self) -> None:
        manifest = build_agent_ecosystem_manifest()
        self.assertEqual(manifest["title"], "Agent-ready three-repository ecosystem")
        self.assertIn("autoscript-public", [repo["name"] for repo in manifest["repositories"]])
        self.assertIn("clawscript-public", [repo["name"] for repo in manifest["repositories"]])

    def test_agent_handoff_manifest(self) -> None:
        manifest = build_agent_handoff_manifest()
        self.assertEqual(manifest["title"], "Agent handoff map")
        self.assertEqual(manifest["handoffs"][0]["stage"], "plan")

    def test_agent_markdown(self) -> None:
        markdown = build_agent_markdown()
        self.assertIn("# Agent Collaboration", markdown)
        self.assertIn("autoSampler-public", markdown)


if __name__ == "__main__":
    unittest.main()
