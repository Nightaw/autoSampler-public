from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import build_showcase_manifest, dump_json


def main() -> int:
    output_path = ROOT / "docs" / "showcase_manifest.json"
    dump_json(output_path, build_showcase_manifest())
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

