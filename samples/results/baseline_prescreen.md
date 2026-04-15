# Baseline Label Prescreen

Mock prescreen service that evaluates a sampled unit, extracts stall and resolution evidence, and returns a structured review report.

## Summary

- Final decision: pass
- Final score: 100
- Stall count: 2
- Resolution events: 3
- Work duration: 18.0s

## Execution Steps

- `load_unit_metadata` | passed | 0.0s | Loaded description.json and label_infos.json
- `inspect_video_metadata` | passed | 0.056s | Collected video duration, size, and dimensions
- `score_heuristics` | passed | 0.0s | Computed rule score=100
- `render_storyboards` | passed | 0.381s | Rendered storyboard artifacts when ffmpeg and Pillow were available
- `persist_report` | passed | 0.0s | Persisted JSON and Markdown reports to tmp/demo_runs

## Metrics

- Video duration: 18.0s
- Longest stall: 1.6s
- Bandwidth hint: 180 kbps

## Artifacts

- report_json: tmp/demo_runs/baseline_prescreen/report.json
- report_markdown: tmp/demo_runs/baseline_prescreen/report.md
- stall_storyboard: tmp/demo_runs/baseline_prescreen/stall_storyboard.jpg
- resolution_storyboard: tmp/demo_runs/baseline_prescreen/resolution_storyboard.jpg
- sample_payload: samples/payloads/baseline_prescreen.json
- sample_unit: samples/units/20260324190033