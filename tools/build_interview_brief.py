from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import build_showcase_manifest, load_json


def build_markdown() -> str:
    manifest = build_showcase_manifest()
    baseline = load_json(ROOT / "samples" / "results" / "baseline_prescreen.json")
    review = load_json(ROOT / "samples" / "results" / "resolution_consistency_review.json")
    return f"""# Interview Brief

## 30-Second Summary

`autoSampler-public` packages a post-capture media-quality review flow into a small worker-style public project.  
The core pipeline covers sample-unit ingestion, device selection, scenario execution planning, heuristic validation for stall and resolution labels, storyboard evidence generation, and structured report delivery through CLI and API entry points.

## 2-Minute Walkthrough

1. A sample unit enters the pipeline with `description.json`, `label_infos.json`, and an attached recording.
2. The runner resolves a mock execution target from the device registry and expands a scenario into an ordered execution plan.
3. The scorer validates stall and resolution labels against timing windows and bandwidth constraints.
4. Storyboard images are generated from selected timestamps to support manual inspection.
5. JSON, Markdown, and showcase artifacts are published for both machine consumption and portfolio display.

## Why This Repo Exists

- Turn a manual review task into a repeatable execution unit.
- Show project structure rather than a loose set of scripts.
- Keep a public-facing repo that still looks like a real service slice.

## Key Talking Points

- The project separates device abstraction, scenario planning, scoring logic, and artifact formatting.
- The public repo includes both a clean baseline case and a review-worthy edge case.
- The same underlying outputs feed API responses, Markdown summaries, static showcase pages, and generated SVG exports.
- Tests and GitHub Actions keep the repo credible as a maintained project, not a one-off upload.

## Scenario Snapshot

- Baseline scenario id: `baseline_prescreen`
- Review scenario id: `resolution_consistency_review`

### Baseline

- Decision: `{baseline['summary']['final_decision']}`
- Score: `{baseline['summary']['final_score']}`
- Stalls: `{baseline['summary']['stall_count']}`
- Resolution events: `{baseline['summary']['resolution_count']}`

### Review Case

- Decision: `{review['summary']['final_decision']}`
- Score: `{review['summary']['final_score']}`
- Warnings:
{chr(10).join(f"- {item}" for item in review['metrics']['heuristic']['warnings'])}

## Portfolio Assets

- `docs/index.html`
- `docs/generated/architecture-export.svg`
- `docs/generated/scenario-comparison.svg`
- `docs/generated/device-capability-matrix.svg`
- `samples/results/stall_storyboard.jpg`
- `samples/results/resolution_review_storyboard.jpg`

## Expected Questions

### Why not publish the full internal repo?

The public repo is curated to preserve system shape without exposing internal infrastructure, credentials, or business-specific assets.

### What shows engineering maturity here?

The main signal is not the individual parser; it is the layering: scenario model, execution planning, device abstraction, evidence generation, multi-surface outputs, and CI-backed packaging.

### What would the next step be?

Attach a richer scenario template system, add more artifact types, and back the mock queue with a small persistence layer.

## Repo Snapshot

- Scenarios: {len(manifest['scenarios'])}
- Showcase artifacts: {len(manifest['storyboards'])}
- Project tagline: `{manifest['tagline']}`
"""


def main() -> int:
    output_path = ROOT / "docs" / "interview-brief.md"
    output_path.write_text(build_markdown(), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
