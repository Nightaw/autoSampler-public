from __future__ import annotations

from common.models import DeviceInfo


DEVICES: tuple[DeviceInfo, ...] = (
    DeviceInfo(
        device_id="ios-lab-01",
        platform="ios",
        os_version="18.1",
        model="iPhone 15 Pro",
        role="capture",
        tags=("primary", "storyboard"),
        capabilities=("video_capture", "touch_replay", "resolution_probe"),
    ),
    DeviceInfo(
        device_id="android-lab-02",
        platform="android",
        os_version="15",
        model="Pixel 8 Pro",
        role="capture",
        tags=("backup", "metrics"),
        capabilities=("video_capture", "adb_shell", "network_profile"),
    ),
    DeviceInfo(
        device_id="android-orch-01",
        platform="android",
        os_version="14",
        model="OnePlus 12",
        role="orchestrator",
        tags=("queue", "worker"),
        capabilities=("job_dispatch", "artifact_sync"),
    ),
)


def list_devices(platform: str | None = None, role: str | None = None) -> list[dict]:
    items = []
    for device in DEVICES:
        if platform and device.platform != platform:
            continue
        if role and device.role != role:
            continue
        items.append(device.to_dict())
    return items


def select_devices(preferred_platforms: tuple[str, ...], preferred_role: str) -> list[dict]:
    selected = [device.to_dict() for device in DEVICES if device.platform in preferred_platforms and device.role == preferred_role]
    if selected:
        return selected[:1]
    fallback = [device.to_dict() for device in DEVICES if device.role == preferred_role]
    return fallback[:1] if fallback else [DEVICES[0].to_dict()]

