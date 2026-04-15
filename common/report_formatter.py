from __future__ import annotations


def render_markdown_report(report: dict) -> str:
    scenario = report["scenario"]
    summary = report["summary"]
    metrics = report["metrics"]
    lines = [
        f"# {scenario['title']}",
        "",
        scenario["description"],
        "",
        "## Summary",
        "",
        f"- Final decision: {summary['final_decision']}",
        f"- Final score: {summary['final_score']}",
        f"- Stall count: {summary['stall_count']}",
        f"- Resolution events: {summary['resolution_count']}",
        f"- Work duration: {summary['work_duration_seconds']}s",
        "",
        "## Devices",
        "",
    ]
    for device in report["devices"]:
        lines.append(
            f"- `{device['device_id']}` | {device['platform']} {device['os_version']} | {device['model']} | {device['role']}"
        )

    lines.extend([
        "",
        "## Execution Steps",
        "",
    ])
    for step in report["execution"]["steps"]:
        lines.append(f"- `{step['name']}` | {step['status']} | {step['duration_sec']}s | {step['details']}")

    lines.extend(["", "## Metrics", ""])
    lines.append(f"- Video duration: {metrics['video_info'].get('duration', 0.0)}s")
    lines.append(f"- Longest stall: {summary['longest_stall_seconds']}s")
    lines.append(f"- Bandwidth hint: {summary['bandwidth_kbps']} kbps")
    lines.append(f"- Execution profile: {report['execution']['profile']}")

    if metrics["heuristic"]["reasons"]:
        lines.extend(["", "## Reasons", ""])
        for item in metrics["heuristic"]["reasons"]:
            lines.append(f"- {item}")

    if metrics["heuristic"]["warnings"]:
        lines.extend(["", "## Warnings", ""])
        for item in metrics["heuristic"]["warnings"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Artifacts", ""])
    for key, value in report["artifacts"].items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)
