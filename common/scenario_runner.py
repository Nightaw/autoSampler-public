from __future__ import annotations

from time import perf_counter

from common.models import ScenarioDefinition, StepResult


STEP_DETAILS: dict[str, str] = {
    "resolve_device": "Matched scenario constraints against the mock device registry.",
    "load_unit_metadata": "Loaded unit description and label metadata into memory.",
    "inspect_video_metadata": "Read recording duration, size, and frame rate via ffprobe.",
    "build_execution_plan": "Expanded the scenario into a deterministic worker-side execution plan.",
    "score_heuristics": "Evaluated stall and resolution labels against bandwidth and timing rules.",
    "render_storyboards": "Rendered storyboard evidence from selected video timestamps.",
    "persist_report": "Wrote JSON and Markdown artifacts for downstream inspection.",
}


PROFILE_STEP_PREFIXES: dict[str, tuple[str, ...]] = {
    "prescreen": ("resolve_device", "build_execution_plan"),
    "resolution_audit": ("resolve_device",),
}


def build_execution_plan(scenario: ScenarioDefinition, selected_devices: list[dict]) -> dict:
    device = selected_devices[0] if selected_devices else None
    return {
        "profile": scenario.execution_profile,
        "device_id": device["device_id"] if device else None,
        "device_role": device["role"] if device else None,
        "focus": list(scenario.focus),
        "steps": list(PROFILE_STEP_PREFIXES.get(scenario.execution_profile, ())) + list(scenario.steps),
    }


def record_step(name: str, started_at: float, details: str | None = None) -> StepResult:
    return StepResult(
        name=name,
        status="passed",
        duration_sec=round(perf_counter() - started_at, 3),
        details=details or STEP_DETAILS.get(name, "Completed."),
    )

