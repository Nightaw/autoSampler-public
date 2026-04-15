from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class ScenarioDefinition:
    name: str
    title: str
    description: str
    unit_dir: str
    steps: tuple[str, ...]
    focus: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class StepResult:
    name: str
    status: str
    duration_sec: float
    details: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class JobReport:
    scenario: dict
    execution: dict
    metrics: dict
    summary: dict
    artifacts: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "scenario": self.scenario,
            "execution": self.execution,
            "metrics": self.metrics,
            "summary": self.summary,
            "artifacts": self.artifacts,
        }

