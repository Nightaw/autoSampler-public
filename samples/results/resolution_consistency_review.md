# Resolution Consistency Review

Resolution-oriented audit path that highlights self-consistency issues between bandwidth constraints, labeled events, and final playback quality.

## Summary

- Final decision: review
- Final score: 82
- Stall count: 3
- Resolution events: 1
- Work duration: 18.0s

## Devices

- `ios-lab-01` | ios 18.1 | iPhone 15 Pro | capture

## Execution Steps

- `resolve_device` | passed | 0.0s | Selected ios-lab-01 for resolution_audit
- `load_unit_metadata` | passed | 0.0s | Loaded unit description and label metadata into memory.
- `inspect_video_metadata` | passed | 0.025s | Read recording duration, size, and frame rate via ffprobe.
- `build_execution_plan` | passed | 0.0s | Expanded to 6 execution steps
- `score_heuristics` | passed | 0.0s | Computed rule score=82 and decision=review
- `render_storyboards` | passed | 0.377s | Rendered storyboard evidence from selected video timestamps.
- `persist_report` | passed | 0.0s | Wrote JSON and Markdown artifacts for downstream inspection.

## Metrics

- Video duration: 18.0s
- Longest stall: 1.2s
- Bandwidth hint: 180 kbps
- Execution profile: resolution_audit

## Warnings

- Detected 1 overlapping stall intervals.
- Final resolution remained unusually high for the available bandwidth.
- Resolution trajectory is too sparse for a constrained-network run.

## Artifacts

- report_json: tmp/demo_runs/resolution_consistency_review/report.json
- report_markdown: tmp/demo_runs/resolution_consistency_review/report.md
- stall_storyboard: tmp/demo_runs/resolution_consistency_review/stall_storyboard.jpg
- resolution_storyboard: tmp/demo_runs/resolution_consistency_review/resolution_storyboard.jpg
- sample_payload: samples/payloads/resolution_consistency_review.json
- sample_unit: samples/units/20260324195510