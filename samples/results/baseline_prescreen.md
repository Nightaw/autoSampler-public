# Baseline Label Prescreen

Mock prescreen worker that evaluates a sampled unit, extracts storyboard evidence, and emits structured review artifacts.

## Summary

- Final decision: pass
- Final score: 100
- Stall count: 2
- Resolution events: 3
- Work duration: 18.0s

## Devices

- `ios-lab-01` | ios 18.1 | iPhone 15 Pro | capture

## Execution Steps

- `resolve_device` | passed | 0.0s | Selected ios-lab-01 for prescreen
- `load_unit_metadata` | passed | 0.0s | Loaded unit description and label metadata into memory.
- `inspect_video_metadata` | passed | 0.022s | Read recording duration, size, and frame rate via ffprobe.
- `build_execution_plan` | passed | 0.0s | Expanded to 7 execution steps
- `score_heuristics` | passed | 0.0s | Computed rule score=100 and decision=pass
- `render_storyboards` | passed | 0.353s | Rendered storyboard evidence from selected video timestamps.
- `persist_report` | passed | 0.0s | Wrote JSON and Markdown artifacts for downstream inspection.

## Metrics

- Video duration: 18.0s
- Longest stall: 1.6s
- Bandwidth hint: 180 kbps
- Execution profile: prescreen

## Artifacts

- report_json: tmp/demo_runs/baseline_prescreen/report.json
- report_markdown: tmp/demo_runs/baseline_prescreen/report.md
- stall_storyboard: tmp/demo_runs/baseline_prescreen/stall_storyboard.jpg
- resolution_storyboard: tmp/demo_runs/baseline_prescreen/resolution_storyboard.jpg
- sample_payload: samples/payloads/baseline_prescreen.json
- sample_unit: samples/units/20260324190033