from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import build_artifact_schema, build_scenario_template_manifest


def main() -> int:
    docs = ROOT / "docs"
    (docs / "artifact-schema.json").write_text(
        json.dumps(build_artifact_schema(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (docs / "scenario-templates.json").write_text(
        json.dumps(build_scenario_template_manifest(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(docs / "artifact-schema.json")
    print(docs / "scenario-templates.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
