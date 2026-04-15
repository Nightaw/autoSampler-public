from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import itertools

from common.prescreen_runner import run_demo_scenario
from common.state import JOB_STATE


_ID_COUNTER = itertools.count(1)
_QUEUE: list[dict] = []
_HISTORY: list[dict] = []


def _timestamp() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _next_job_id() -> str:
    return f"job-{next(_ID_COUNTER):04d}"


def enqueue_job(scenario: str) -> dict:
    job = {
        "job_id": _next_job_id(),
        "scenario": scenario,
        "status": "queued",
        "created_at": _timestamp(),
        "started_at": None,
        "finished_at": None,
        "report": None,
    }
    _QUEUE.append(job)
    JOB_STATE.status = "queued"
    JOB_STATE.current_scenario = scenario
    return deepcopy(job)


def list_jobs() -> list[dict]:
    return [deepcopy(job) for job in (_QUEUE + _HISTORY)]


def get_job(job_id: str) -> dict | None:
    for job in _QUEUE + _HISTORY:
        if job["job_id"] == job_id:
            return deepcopy(job)
    return None


def process_next_job() -> dict | None:
    if not _QUEUE:
        return None
    job = _QUEUE.pop(0)
    job["status"] = "running"
    job["started_at"] = _timestamp()
    JOB_STATE.status = "running"
    JOB_STATE.current_scenario = job["scenario"]

    report = run_demo_scenario(job["scenario"])
    job["report"] = report
    job["status"] = "finished"
    job["finished_at"] = _timestamp()

    JOB_STATE.status = "finished"
    JOB_STATE.completed_steps = len(report["execution"]["steps"])
    JOB_STATE.last_report_path = report["artifacts"]["report_json"]

    _HISTORY.append(job)
    return deepcopy(job)


def reset_jobs() -> None:
    _QUEUE.clear()
    _HISTORY.clear()
    JOB_STATE.status = "idle"
    JOB_STATE.current_scenario = None
    JOB_STATE.completed_steps = 0
    JOB_STATE.last_report_path = None

