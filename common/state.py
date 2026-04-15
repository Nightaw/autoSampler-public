from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JobState:
    status: str = "idle"
    current_scenario: str | None = None
    completed_steps: int = 0
    last_report_path: str | None = None


JOB_STATE = JobState()

