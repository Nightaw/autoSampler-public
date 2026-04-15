from __future__ import annotations

from dataclasses import asdict
import json
import math
import shutil
import subprocess
from pathlib import Path
from time import perf_counter
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:  # pragma: no cover - optional runtime dependency
    Image = None
    ImageDraw = None
    ImageFont = None
    ImageOps = None

from common.models import JobReport, ScenarioDefinition, StepResult
from common.report_formatter import render_markdown_report


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"
TMP_ROOT = ROOT / "tmp" / "demo_runs"


SCENARIOS: dict[str, ScenarioDefinition] = {
    "baseline_prescreen": ScenarioDefinition(
        name="baseline_prescreen",
        title="Baseline Label Prescreen",
        description=(
            "Mock prescreen service that evaluates a sampled unit, extracts stall and "
            "resolution evidence, and returns a structured review report."
        ),
        unit_dir="units/20260324190033",
        steps=(
            "load_unit_metadata",
            "inspect_video_metadata",
            "score_heuristics",
            "render_storyboards",
            "persist_report",
        ),
        focus=("stall", "resolution", "report"),
    ),
    "resolution_consistency_review": ScenarioDefinition(
        name="resolution_consistency_review",
        title="Resolution Consistency Review",
        description=(
            "Mock scenario focused on whether resolution labels remain self-consistent "
            "under constrained bandwidth conditions."
        ),
        unit_dir="units/20260324190033",
        steps=(
            "load_unit_metadata",
            "inspect_video_metadata",
            "score_heuristics",
            "persist_report",
        ),
        focus=("resolution", "sanity_check"),
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2, ensure_ascii=False)


def to_pretty_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


def list_scenarios() -> list[dict]:
    return [scenario.to_dict() for scenario in SCENARIOS.values()]


def describe_architecture() -> dict[str, Any]:
    return {
        "scenario_count": len(SCENARIOS),
        "pipeline_layers": [
            "unit fixtures",
            "heuristic scorer",
            "storyboard generator",
            "markdown formatter",
            "flask demo api",
        ],
        "artifact_roots": [
            "samples/units",
            "samples/payloads",
            "samples/results",
            "tmp/demo_runs",
        ],
    }


def parse_frame_rate(raw_value: str) -> float | None:
    if not raw_value:
        return None
    if "/" in raw_value:
        numerator, denominator = raw_value.split("/", 1)
        try:
            denominator_value = float(denominator)
            if abs(denominator_value) < 1e-9:
                return None
            return float(numerator) / denominator_value
        except ValueError:
            return None
    try:
        return float(raw_value)
    except ValueError:
        return None


def ffprobe_video(video_path: Path | None) -> dict[str, Any]:
    if not video_path or not video_path.exists() or shutil.which("ffprobe") is None:
        return {}
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size",
        "-show_entries",
        "stream=width,height,r_frame_rate",
        "-of",
        "json",
        str(video_path),
    ]
    try:
        completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return {}
    payload = json.loads(completed.stdout or "{}")
    format_info = payload.get("format", {})
    streams = payload.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("width")), {})
    return {
        "duration": round(float(format_info.get("duration") or 0.0), 3),
        "size_bytes": int(format_info.get("size") or 0),
        "width": int(video_stream.get("width") or 0),
        "height": int(video_stream.get("height") or 0),
        "frame_rate": parse_frame_rate(str(video_stream.get("r_frame_rate") or "")),
    }


def clamp_time(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def seconds_to_text(value: float) -> str:
    minutes, seconds = divmod(max(0.0, float(value)), 60.0)
    return f"{int(minutes):02}:{seconds:05.2f}"


def choose_stall_samples(
    stalls: list[dict[str, float]],
    work_start: float,
    work_duration: float,
    max_events: int,
) -> list[dict[str, Any]]:
    if not stalls:
        return []
    ranked = sorted(
        stalls,
        key=lambda item: (float(item["end"]) - float(item["start"]), -float(item["start"])),
        reverse=True,
    )
    selected = sorted(ranked[: max(1, max_events)], key=lambda item: float(item["start"]))
    samples: list[dict[str, Any]] = []
    for index, item in enumerate(selected, start=1):
        start_offset = clamp_time(float(item["start"]) - work_start, 0.0, work_duration)
        end_offset = clamp_time(float(item["end"]) - work_start, 0.0, work_duration)
        duration = max(0.0, end_offset - start_offset)
        mid_offset = clamp_time(start_offset + duration / 2.0, 0.0, work_duration)
        samples.extend(
            [
                {"offset": clamp_time(start_offset - 0.35, 0.0, work_duration), "caption": f"stall#{index} before"},
                {"offset": mid_offset, "caption": f"stall#{index} mid {seconds_to_text(duration)}"},
                {"offset": clamp_time(end_offset + 0.35, 0.0, work_duration), "caption": f"stall#{index} after"},
            ]
        )
    return samples


def choose_resolution_samples(
    resolutions: list[dict[str, Any]],
    work_start: float,
    work_duration: float,
    max_events: int,
) -> list[dict[str, Any]]:
    if not resolutions:
        return []
    selected = sorted(resolutions[: max(1, max_events)], key=lambda item: float(item.get("time") or 0.0))
    return [
        {
            "offset": clamp_time(float(item.get("time") or work_start) - work_start, 0.0, work_duration),
            "caption": f"res#{index} {item.get('resolution', 'unknown')}",
        }
        for index, item in enumerate(selected, start=1)
    ]


def extract_frame(video_path: Path, offset_seconds: float, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{max(0.0, offset_seconds):.3f}",
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-vf",
        "scale=480:-1",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)
    return output_path


def build_storyboard(title: str, samples: list[dict[str, Any]], video_path: Path, output_path: Path) -> Path | None:
    if not samples or Image is None or shutil.which("ffmpeg") is None:
        return None

    frame_paths: list[tuple[Path, str]] = []
    frame_root = output_path.parent / f"{output_path.stem}_frames"
    frame_root.mkdir(parents=True, exist_ok=True)
    for index, sample in enumerate(samples, start=1):
        frame_path = frame_root / f"{index:02d}.jpg"
        extract_frame(video_path, float(sample["offset"]), frame_path)
        frame_paths.append((frame_path, f"{sample['caption']}\n@ {seconds_to_text(sample['offset'])}"))

    margin = 24
    gap = 16
    caption_height = 60
    title_height = 72
    cell_width = 360
    cell_height = 220
    columns = 3
    rows = int(math.ceil(len(frame_paths) / columns))

    canvas = Image.new(
        "RGB",
        (
            margin * 2 + columns * cell_width + (columns - 1) * gap,
            margin * 2 + title_height + rows * (cell_height + caption_height) + max(0, rows - 1) * gap,
        ),
        color=(248, 248, 250),
    )
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    draw.text((margin, margin), title, fill=(20, 24, 36), font=title_font)

    for index, (frame_path, caption) in enumerate(frame_paths):
        row = index // columns
        col = index % columns
        x = margin + col * (cell_width + gap)
        y = margin + title_height + row * (cell_height + caption_height + gap)
        raw = Image.open(frame_path).convert("RGB")
        framed = ImageOps.contain(raw, (cell_width, cell_height))
        frame_x = x + (cell_width - framed.width) // 2
        frame_y = y + (cell_height - framed.height) // 2
        canvas.paste(framed, (frame_x, frame_y))
        draw.rectangle((x, y, x + cell_width, y + cell_height), outline=(205, 210, 220), width=2)
        draw.multiline_text((x, y + cell_height + 8), caption, fill=(66, 69, 82), font=body_font, spacing=4)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, quality=90)
    return output_path


def parse_bandwidth_kbps(description: dict[str, Any]) -> int | None:
    raw_network = description.get("networkSide_down_param") or {}
    raw = str(raw_network.get("bandwidth") or "").strip().lower()
    digits = "".join(char for char in raw if char.isdigit())
    return int(digits) if digits else None


def score_heuristics(
    description: dict[str, Any],
    labels: dict[str, Any],
    video_info: dict[str, Any],
) -> dict[str, Any]:
    work_start = float(labels.get("work_start_time") or 0.0)
    work_end = float(labels.get("work_end_time") or 0.0)
    work_duration = max(0.0, work_end - work_start)
    stalls = sorted(labels.get("stall") or [], key=lambda item: float(item.get("start") or 0.0))
    resolutions = sorted(labels.get("resolution") or [], key=lambda item: float(item.get("time") or 0.0))
    bandwidth_kbps = parse_bandwidth_kbps(description)

    score = 100
    reasons: list[str] = []
    warnings: list[str] = []

    if work_duration <= 1.0:
        score -= 45
        reasons.append("工作区间异常，无法形成有效时长。")

    total_stall_duration = 0.0
    longest_stall = 0.0
    invalid_stalls = 0
    for stall in stalls:
        start = float(stall.get("start") or 0.0)
        end = float(stall.get("end") or 0.0)
        duration = end - start
        if duration <= 0:
            invalid_stalls += 1
            continue
        total_stall_duration += duration
        longest_stall = max(longest_stall, duration)
        if work_duration > 1.0 and (start < work_start - 1.0 or end > work_end + 1.0):
            invalid_stalls += 1

    if invalid_stalls:
        score -= min(24, invalid_stalls * 8)
        reasons.append(f"检测到 {invalid_stalls} 条 stall 标注越界或时长异常。")

    stall_ratio = total_stall_duration / work_duration if work_duration > 1.0 else None
    if stall_ratio is not None and stall_ratio > 0.7:
        score -= 10
        warnings.append(f"stall 占比达到 {stall_ratio * 100:.1f}%，建议复核。")

    if bandwidth_kbps is not None and bandwidth_kbps <= 200 and stall_ratio is not None and stall_ratio < 0.01:
        score -= 8
        warnings.append("低带宽条件下几乎没有 stall，标签可能偏保守。")

    if not resolutions:
        score -= 25
        reasons.append("缺少 resolution 事件，无法确认清晰度变化链路。")

    if bandwidth_kbps is not None and resolutions:
        last_raw = str(resolutions[-1].get("resolution_raw") or "")
        if bandwidth_kbps <= 200 and "1080" in last_raw:
            score -= 8
            warnings.append("低带宽下最终分辨率仍过高，建议复核。")

    if not video_info:
        warnings.append("未获取到录屏元信息，本次仅基于结构化标签评分。")

    score = max(0, min(100, score))
    if score >= 85:
        decision = "pass"
    elif score >= 60:
        decision = "review"
    else:
        decision = "reject"

    return {
        "score": score,
        "decision": decision,
        "reasons": reasons,
        "warnings": warnings,
        "summary": {
            "bandwidth_kbps": bandwidth_kbps,
            "work_duration_seconds": round(work_duration, 3),
            "stall_count": len(stalls),
            "stall_total_seconds": round(total_stall_duration, 3),
            "longest_stall_seconds": round(longest_stall, 3),
            "resolution_count": len(resolutions),
            "video_duration_seconds": round(float(video_info.get("duration") or 0.0), 3),
        },
    }


def _step(name: str, start_time: float, details: str) -> StepResult:
    return StepResult(name=name, status="passed", duration_sec=round(perf_counter() - start_time, 3), details=details)


def _scenario_unit_dir(name: str) -> Path:
    scenario = SCENARIOS[name]
    return SAMPLES / scenario.unit_dir


def _artifact_path(output_dir: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    return str(path.relative_to(ROOT))


def run_demo_scenario(name: str) -> dict[str, Any]:
    if name not in SCENARIOS:
        raise KeyError(f"Unknown scenario: {name}")

    scenario = SCENARIOS[name]
    unit_dir = _scenario_unit_dir(name)
    output_dir = TMP_ROOT / name
    output_dir.mkdir(parents=True, exist_ok=True)
    steps: list[StepResult] = []

    start = perf_counter()
    description = load_json(unit_dir / "20260324190033_description.json")
    labels = load_json(unit_dir / "20260324190033_label_infos.json")
    steps.append(_step("load_unit_metadata", start, "Loaded description.json and label_infos.json"))

    start = perf_counter()
    video_path = unit_dir / "20260324190033_main_scrcpy.mp4"
    video_info = ffprobe_video(video_path if video_path.exists() else None)
    steps.append(_step("inspect_video_metadata", start, "Collected video duration, size, and dimensions"))

    start = perf_counter()
    heuristic = score_heuristics(description, labels, video_info)
    steps.append(_step("score_heuristics", start, f"Computed rule score={heuristic['score']}"))

    work_start = float(labels.get("work_start_time") or 0.0)
    work_end = float(labels.get("work_end_time") or 0.0)
    work_duration = max(0.0, work_end - work_start)

    start = perf_counter()
    stall_board = None
    resolution_board = None
    if video_path.exists() and work_duration > 1.0:
        stall_board = build_storyboard(
            title=f"{scenario.name} stall storyboard",
            samples=choose_stall_samples(labels.get("stall") or [], work_start, work_duration, 3),
            video_path=video_path,
            output_path=output_dir / "stall_storyboard.jpg",
        )
        resolution_board = build_storyboard(
            title=f"{scenario.name} resolution storyboard",
            samples=choose_resolution_samples(labels.get("resolution") or [], work_start, work_duration, 3),
            video_path=video_path,
            output_path=output_dir / "resolution_storyboard.jpg",
        )
    steps.append(_step("render_storyboards", start, "Rendered storyboard artifacts when ffmpeg and Pillow were available"))

    summary = {
        "unit_id": description.get("unit_id"),
        "final_decision": heuristic["decision"],
        "final_score": heuristic["score"],
        "bandwidth_kbps": heuristic["summary"]["bandwidth_kbps"],
        "work_duration_seconds": heuristic["summary"]["work_duration_seconds"],
        "stall_count": heuristic["summary"]["stall_count"],
        "longest_stall_seconds": heuristic["summary"]["longest_stall_seconds"],
        "resolution_count": heuristic["summary"]["resolution_count"],
        "scenario": description.get("requirement_scenario") or description.get("需求场景"),
        "app_version": description.get("app_version"),
    }
    metrics = {
        "video_info": video_info,
        "label_summary": {
            "stall": labels.get("stall") or [],
            "resolution": labels.get("resolution") or [],
        },
        "heuristic": heuristic,
    }

    report = JobReport(
        scenario=asdict(scenario),
        execution={
            "status": "passed",
            "steps": [step.to_dict() for step in steps],
        },
        metrics=metrics,
        summary=summary,
        artifacts={},
    )
    report_dict = report.to_dict()

    start = perf_counter()
    report_json_path = output_dir / "report.json"
    report_md_path = output_dir / "report.md"
    dump_json(report_json_path, report_dict)
    report_md_path.write_text(render_markdown_report(report_dict), encoding="utf-8")
    steps.append(_step("persist_report", start, "Persisted JSON and Markdown reports to tmp/demo_runs"))

    report_dict["execution"]["steps"] = [step.to_dict() for step in steps]
    report_dict["artifacts"] = {
        "report_json": _artifact_path(output_dir, report_json_path),
        "report_markdown": _artifact_path(output_dir, report_md_path),
        "stall_storyboard": _artifact_path(output_dir, stall_board),
        "resolution_storyboard": _artifact_path(output_dir, resolution_board),
        "sample_payload": "samples/payloads/baseline_prescreen.json",
        "sample_unit": str(unit_dir.relative_to(ROOT)),
    }
    dump_json(report_json_path, report_dict)
    report_md_path.write_text(render_markdown_report(report_dict), encoding="utf-8")
    return report_dict


def build_markdown_report(name: str) -> str:
    return render_markdown_report(run_demo_scenario(name))

