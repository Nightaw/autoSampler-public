from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import build_artifact_schema, build_scenario_template_manifest


class ContractDocsTest(unittest.TestCase):
    def test_template_manifest(self) -> None:
        manifest = build_scenario_template_manifest()
        self.assertEqual(manifest["project"], "autoSampler Public")
        self.assertGreaterEqual(len(manifest["templates"]), 3)

    def test_artifact_schema_shape(self) -> None:
        schema = build_artifact_schema()
        self.assertEqual(schema["title"], "autoSampler Public Artifact Manifest")
        self.assertIn("artifact_groups", schema["properties"])


if __name__ == "__main__":
    unittest.main()
