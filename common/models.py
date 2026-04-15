from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class DeviceInfo:
    device_id: str
    platform: str
    os_version: str
    model: str
    role: str
    tags: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ScenarioDefinition:
    name: str
    title: str
    description: str
    unit_dir: str
    steps: tuple[str, ...]
    focus: tuple[str, ...]
    preferred_platforms: tuple[str, ...]
    preferred_role: str
    execution_profile: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ScenarioTemplate:
    template_id: str
    title: str
    description: str
    scenario: str
    steps: tuple[str, ...]
    outputs: tuple[str, ...]
    trigger: str

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
    devices: list[dict]
    execution: dict
    metrics: dict
    summary: dict
    artifacts: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "scenario": self.scenario,
            "devices": self.devices,
            "execution": self.execution,
            "metrics": self.metrics,
            "summary": self.summary,
            "artifacts": self.artifacts,
        }
