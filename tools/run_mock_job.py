from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import list_scenarios, run_demo_scenario, to_pretty_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the mock prescreen job and print a structured report."
    )
    parser.add_argument(
        "--scenario",
        default="baseline_prescreen",
        help="Scenario name. Use --list to inspect available scenarios.",
    )
    parser.add_argument("--list", action="store_true", help="List scenarios and exit.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.list:
        print(to_pretty_json({"scenarios": list_scenarios()}))
        return 0

    print(to_pretty_json(run_demo_scenario(args.scenario)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

