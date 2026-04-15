# Showcase Notes

## Intended Narrative

The repository is organized around a single engineering story:

1. A sampled unit arrives with metadata and a screen recording.
2. A worker-style runner selects an execution target from a mock device registry.
3. The scenario is expanded into an execution plan.
4. Heuristic review evaluates stall and resolution labels.
5. Storyboard artifacts are generated for manual verification.
6. The system emits JSON and Markdown outputs and exposes them through an API.

## Assets Suitable for a Portfolio Page

- `docs/hero.svg`
- `samples/results/stall_storyboard.jpg`
- `samples/results/resolution_storyboard.jpg`
- `samples/results/resolution_review_storyboard.jpg`
- `samples/results/baseline_prescreen.json`
- `samples/results/resolution_consistency_review.json`

## Interview-Friendly Angles

- Conversion of a manual review task into a repeatable worker pipeline
- Separation between device abstraction, scenario planning, scoring, and reporting
- Artifact design for both machines and human reviewers
- Public repo packaging with tests and CI instead of a loose script collection

