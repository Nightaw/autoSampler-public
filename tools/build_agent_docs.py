from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import build_agent_ecosystem_manifest, build_agent_handoff_manifest


def build_markdown() -> str:
    ecosystem = build_agent_ecosystem_manifest()
    handoffs = build_agent_handoff_manifest()
    repo_lines = "\n".join(
        [
            f"- `{repo['name']}` ({repo['status']}): {repo['role']}. Handoff: {repo['handoff']}."
            for repo in ecosystem["repositories"]
        ]
    )
    handoff_lines = "\n".join(
        [
            f"- `{item['stage']}` -> `{item['owner']}`: input `{item['input']}`; output `{item['output']}`."
            for item in handoffs["handoffs"]
        ]
    )
    contract_lines = "\n".join(f"- `{item}`" for item in ecosystem["shared_contracts"])

    return f"""# Agent Collaboration

`autoSampler-public` is positioned as one layer in a broader agent-ready project system. The public narrative separates orchestration, execution, and evidence packaging so each repository has a clear reason to exist.

## Repository Roles

{repo_lines}

## Handoff Flow

{handoff_lines}

## Shared Contracts

{contract_lines}

## Interview Framing

{handoffs['interview_message']}

For a manufacturing or cloud-device interview, the useful point is the boundary design: an agent can decide what to run, a worker can execute the task, and `autoSampler-public` can turn sample output into reviewable evidence. This makes the portfolio read like a small system rather than a collection of isolated scripts.
"""


def main() -> int:
    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "agent-ecosystem.json").write_text(
        json.dumps(build_agent_ecosystem_manifest(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (docs / "agent-handoffs.json").write_text(
        json.dumps(build_agent_handoff_manifest(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (docs / "agent-collaboration.md").write_text(build_markdown(), encoding="utf-8")
    print(docs / "agent-collaboration.md")
    print(docs / "agent-ecosystem.json")
    print(docs / "agent-handoffs.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
