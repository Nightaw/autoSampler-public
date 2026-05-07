# Agent Collaboration

`autoSampler-public` is positioned as one layer in a broader agent-ready project system. The public narrative separates orchestration, execution, and evidence packaging so each repository has a clear reason to exist.

## Repository Roles

- `autoscript-public` (published): worker runtime and playback automation facade. Handoff: accepts planned automation work and returns structured worker reports.
- `autoSampler-public` (published): post-capture sampling, review evidence, and artifact packaging layer. Handoff: turns captured media units into review decisions, images, JSON, Markdown, and site artifacts.
- `clawscript` (planned_public_release): agent workflow orchestration and multi-repository coordination layer. Handoff: coordinates which repo should execute, review, package, or publish each step.

## Handoff Flow

- `plan` -> `clawscript`: input `interview task, operator intent, or regression review request`; output `repo-targeted scenario plan`.
- `execute` -> `autoscript-public`: input `scenario plan and playback target`; output `worker-style run result and parsed playback metrics`.
- `sample-review` -> `autoSampler-public`: input `sample unit, labels, recording, and device profile`; output `decision score, warnings, and review reasons`.
- `package-evidence` -> `autoSampler-public`: input `review report and selected timestamps`; output `storyboards, timelines, Markdown, JSON, and static site assets`.
- `publish` -> `autoSampler-public`: input `generated artifacts and documentation manifests`; output `GitHub Pages bundle and interview walkthrough documents`.

## Shared Contracts

- `scenario templates`
- `structured report JSON`
- `artifact manifest`
- `worker API routes`
- `generated evidence assets`
- `CI and Pages build outputs`

## Interview Framing

The system is framed as an agent-ready workflow: orchestration decides the work, automation executes it, and the sampler produces verifiable evidence.

For a manufacturing or cloud-device interview, the useful point is the boundary design: an agent can decide what to run, a worker can execute the task, and `autoSampler-public` can turn sample output into reviewable evidence. This makes the portfolio read like a small system rather than a collection of isolated scripts.
