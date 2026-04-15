# Interview Brief

## 30-Second Summary

`autoSampler-public` packages a post-capture media-quality review flow into a small worker-style public project.  
The core pipeline covers sample-unit ingestion, device selection, scenario execution planning, heuristic validation for stall and resolution labels, storyboard evidence generation, and structured report delivery through CLI and API entry points.

## 2-Minute Walkthrough

1. A sample unit enters the pipeline with `description.json`, `label_infos.json`, and an attached recording.
2. The runner resolves a mock execution target from the device registry and expands a scenario into an ordered execution plan.
3. The scorer validates stall and resolution labels against timing windows and bandwidth constraints.
4. Storyboard images are generated from selected timestamps to support manual inspection.
5. JSON, Markdown, and showcase artifacts are published for both machine consumption and portfolio display.

## 5-Minute Deep Dive

1. The public repo keeps the same shape as a larger internal workflow by separating device selection, scenario planning, scoring, and artifact formatting.
2. Two sample units are bundled on purpose: one shows the expected success path, and one shows how a review-worthy regression is surfaced.
3. The same report data is reused across API responses, Markdown summaries, SVG exports, case-study pages, and the deployable showcase site.
4. Generated assets are treated as first-class outputs so the project can be explained visually, not only through source code.
5. GitHub Actions validates tests and builds a complete Pages bundle rather than publishing an incomplete docs folder.

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

- Decision: `pass`
- Score: `100`
- Stalls: `2`
- Resolution events: `3`

### Review Case

- Decision: `review`
- Score: `82`
- Warnings:
- Detected 1 overlapping stall intervals.
- Final resolution remained unusually high for the available bandwidth.
- Resolution trajectory is too sparse for a constrained-network run.

## Portfolio Assets

- `docs/index.html`
- `docs/generated/architecture-export.svg`
- `docs/generated/scenario-comparison.svg`
- `docs/generated/device-capability-matrix.svg`
- `samples/results/stall_storyboard.jpg`
- `samples/results/resolution_review_storyboard.jpg`

## Recommended Demo Flow

1. Start with `docs/index.html` or the deployed Pages site to establish the pipeline.
2. Open `docs/interview-brief.md` and use the 30-second or 2-minute version depending on interview pace.
3. Jump into `docs/cases/baseline_prescreen.html` and `docs/cases/resolution_consistency_review.html` to show one pass path and one review path.
4. Use `docs/generated/scenario-comparison.svg` and `docs/generated/device-capability-matrix.svg` when the discussion shifts toward architecture and extensibility.

## Framework Hooks

- `docs/scenario-templates.json` describes reusable execution templates.
- `docs/artifact-schema.json` documents the shape of the artifact manifest used by the public site and API.
- `GET /demo/templates` and `GET /demo/schemas` expose the same contract surfaces programmatically.

## Expected Questions

### Why not publish the full internal repo?

The public repo is curated to preserve system shape without exposing internal infrastructure, credentials, or business-specific assets.

### What shows engineering maturity here?

The main signal is not the individual parser; it is the layering: scenario model, execution planning, device abstraction, evidence generation, multi-surface outputs, and CI-backed packaging.

### What would the next step be?

Attach a richer scenario template system, add more artifact types, and back the mock queue with a small persistence layer.

## Repo Snapshot

- Scenarios: 2
- Showcase artifacts: 3
- Project tagline: `worker-style media label prescreen demo`
