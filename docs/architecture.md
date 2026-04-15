# Architecture

## End-to-End Flow

1. Load a public sample unit from `samples/units`.
2. Select a mock device from `common/device_registry.py`.
3. Expand a scenario into an execution plan in `common/scenario_runner.py`.
4. Score stall and resolution labels in `common/prescreen_runner.py`.
5. Generate storyboard evidence when `ffmpeg` and Pillow are available.
6. Persist JSON and Markdown artifacts under `tmp/demo_runs`.
7. Expose the same flow through `app/server.py`.

## Modules

### `samples/units`

Public sample units with:

- `*_description.json`
- `*_label_infos.json`
- `*_main_scrcpy.mp4`

### `common/device_registry.py`

Mock inventory for worker-side execution targets.  
The registry exists to make scenario execution look like a real service workflow rather than a direct local script call.

### `common/scenario_runner.py`

Scenario planning layer responsible for:

- profile-specific execution planning
- target selection bookkeeping
- normalized step recording

### `common/prescreen_runner.py`

Core business logic:

- unit loading
- video metadata probing
- heuristic scoring
- storyboard generation
- artifact persistence

### `common/job_queue.py`

Lightweight queue model for:

- enqueue
- list
- process
- detail lookup

### `app/server.py`

REST wrapper around the runner and queue primitives.

## Design Goal

The project keeps the engineering signal of a larger internal workflow while staying small enough to run locally.  
The intent is to show system shape, execution layering, and output design rather than expose production infrastructure.
