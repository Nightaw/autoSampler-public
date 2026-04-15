from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.device_registry import list_devices
from common.prescreen_runner import build_showcase_manifest, load_json


OUT = ROOT / "docs" / "generated"


def wrap_svg(width: int, height: int, body: str) -> str:
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="{width}" height="{height}" rx="28" fill="#FBF8F2"/>
{body}
</svg>
"""


def save(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_architecture_export() -> str:
    body = """
<rect x="42" y="42" width="1116" height="616" rx="24" fill="#F3EEE2" stroke="#D8CFBD"/>
<text x="74" y="96" fill="#1B1F20" font-family="Georgia, serif" font-size="42">autoSampler public flow</text>
<text x="74" y="126" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="18">sample unit to worker API to reviewer-facing artifacts</text>

<rect x="86" y="190" width="200" height="108" rx="18" fill="#183A37"/>
<text x="112" y="236" fill="#FFFDF6" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Sample Unit</text>
<text x="112" y="268" fill="#D4E0D8" font-family="Helvetica, Arial, sans-serif" font-size="16">description + labels + mp4</text>

<rect x="348" y="190" width="220" height="108" rx="18" fill="#476C9B"/>
<text x="374" y="236" fill="#FFFDF6" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Device Registry</text>
<text x="374" y="268" fill="#E1EAF5" font-family="Helvetica, Arial, sans-serif" font-size="16">platform / role / capability match</text>

<rect x="630" y="190" width="220" height="108" rx="18" fill="#BF4C2F"/>
<text x="656" y="236" fill="#FFFDF6" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Execution Plan</text>
<text x="656" y="268" fill="#F7DED8" font-family="Helvetica, Arial, sans-serif" font-size="16">scenario profile + ordered steps</text>

<rect x="912" y="190" width="206" height="108" rx="18" fill="#C79B28"/>
<text x="938" y="236" fill="#2D2614" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Heuristic Review</text>
<text x="938" y="268" fill="#5A4A1F" font-family="Helvetica, Arial, sans-serif" font-size="16">stall / resolution scoring</text>

<rect x="210" y="396" width="250" height="120" rx="18" fill="#EFE5CF"/>
<text x="238" y="444" fill="#1B1F20" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Storyboard Evidence</text>
<text x="238" y="476" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="16">frame extraction for manual review</text>

<rect x="506" y="396" width="250" height="120" rx="18" fill="#E3EBF3"/>
<text x="534" y="444" fill="#1B1F20" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Structured Reports</text>
<text x="534" y="476" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="16">json + markdown + manifest</text>

<rect x="802" y="396" width="196" height="120" rx="18" fill="#E7DDD3"/>
<text x="830" y="444" fill="#1B1F20" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">Worker API</text>
<text x="830" y="476" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="16">run / jobs / showcase</text>

<path d="M286 244H348" stroke="#5F625B" stroke-width="8" stroke-linecap="round"/>
<path d="M568 244H630" stroke="#5F625B" stroke-width="8" stroke-linecap="round"/>
<path d="M850 244H912" stroke="#5F625B" stroke-width="8" stroke-linecap="round"/>
<path d="M1015 298V348H334V396" stroke="#5F625B" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M1015 298V356H631V396" stroke="#5F625B" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M1015 298V396H900" stroke="#5F625B" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
"""
    return wrap_svg(1200, 700, body)


def build_scenario_comparison() -> str:
    manifest = build_showcase_manifest()
    cards = []
    x = 88
    colors = {"pass": "#183A37", "review": "#C79B28", "reject": "#BF4C2F"}
    for item in manifest["scenarios"]:
        summary = item["summary"] or {}
        decision = str(summary.get("final_decision", "review"))
        color = colors.get(decision, "#476C9B")
        score = int(summary.get("final_score", 0))
        bar_height = int(score * 3.4)
        top = 530 - bar_height
        cards.append(
            f"""
<rect x="{x}" y="{top}" width="180" height="{bar_height}" rx="18" fill="{color}"/>
<text x="{x + 24}" y="{top + 42}" fill="#FFFDF6" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="700">{item['title']}</text>
<text x="{x + 24}" y="{top + 78}" fill="#F0F0E8" font-family="Helvetica, Arial, sans-serif" font-size="16">{decision.upper()} / {score}</text>
<text x="{x}" y="584" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="16">stall {summary.get('stall_count')}</text>
<text x="{x}" y="608" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="16">resolution {summary.get('resolution_count')}</text>
"""
        )
        x += 240
    body = f"""
<text x="72" y="90" fill="#1B1F20" font-family="Georgia, serif" font-size="40">scenario comparison</text>
<text x="72" y="120" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="18">score and artifact behavior across bundled sample units</text>
<line x1="72" y1="530" x2="1128" y2="530" stroke="#D8CFBD" stroke-width="2"/>
<text x="72" y="520" fill="#8A857A" font-family="Helvetica, Arial, sans-serif" font-size="14">0</text>
<text x="72" y="210" fill="#8A857A" font-family="Helvetica, Arial, sans-serif" font-size="14">100</text>
{''.join(cards)}
"""
    return wrap_svg(1200, 680, body)


def build_device_matrix() -> str:
    devices = list_devices()
    caps = sorted({cap for device in devices for cap in device["capabilities"]})
    rows = []
    y = 150
    for device in devices:
        rows.append(f'<text x="72" y="{y}" fill="#1B1F20" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700">{device["device_id"]}</text>')
        rows.append(f'<text x="72" y="{y + 24}" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="14">{device["platform"]} / {device["model"]} / {device["role"]}</text>')
        x = 360
        for cap in caps:
            active = cap in device["capabilities"]
            fill = "#183A37" if active else "#E5DED0"
            rows.append(f'<rect x="{x}" y="{y - 18}" width="126" height="36" rx="10" fill="{fill}"/>')
            rows.append(f'<text x="{x + 16}" y="{y + 5}" fill="{"#FFFDF6" if active else "#8A857A"}" font-family="Helvetica, Arial, sans-serif" font-size="14">{cap}</text>')
            x += 138
        y += 92
    body = f"""
<text x="72" y="84" fill="#1B1F20" font-family="Georgia, serif" font-size="40">device capability matrix</text>
<text x="72" y="114" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="18">mock execution targets used by the public scenario planner</text>
{''.join(rows)}
"""
    return wrap_svg(1200, 500, body)


def build_timeline(report_name: str, title: str) -> str:
    report = load_json(ROOT / "samples" / "results" / report_name)
    work_duration = float(report["summary"]["work_duration_seconds"])
    stalls = report["metrics"]["label_summary"]["stall"]
    resolutions = report["metrics"]["label_summary"]["resolution"]
    bars = []
    width = 980
    left = 120
    for stall in stalls:
        start = float(stall["start"]) / work_duration
        end = float(stall["end"]) / work_duration
        x = left + start * width
        w = max(12, (end - start) * width)
        bars.append(f'<rect x="{x:.1f}" y="210" width="{w:.1f}" height="44" rx="12" fill="#BF4C2F"/>')
    markers = []
    for item in resolutions:
        pos = left + (float(item["time"]) / work_duration) * width
        markers.append(f'<circle cx="{pos:.1f}" cy="326" r="13" fill="#476C9B"/>')
        markers.append(f'<text x="{pos - 26:.1f}" y="360" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="14">{item["resolution"]}</text>')
    body = f"""
<text x="72" y="88" fill="#1B1F20" font-family="Georgia, serif" font-size="40">{title}</text>
<text x="72" y="118" fill="#5F625B" font-family="Helvetica, Arial, sans-serif" font-size="18">timeline of stall windows and labeled resolution transitions</text>
<line x1="{left}" y1="232" x2="{left + width}" y2="232" stroke="#D8CFBD" stroke-width="10" stroke-linecap="round"/>
<line x1="{left}" y1="326" x2="{left + width}" y2="326" stroke="#D8CFBD" stroke-width="10" stroke-linecap="round"/>
<text x="72" y="238" fill="#8A857A" font-family="Helvetica, Arial, sans-serif" font-size="15">stall windows</text>
<text x="72" y="332" fill="#8A857A" font-family="Helvetica, Arial, sans-serif" font-size="15">resolution events</text>
<text x="{left}" y="402" fill="#8A857A" font-family="Helvetica, Arial, sans-serif" font-size="14">0s</text>
<text x="{left + width - 44}" y="402" fill="#8A857A" font-family="Helvetica, Arial, sans-serif" font-size="14">{int(work_duration)}s</text>
{''.join(bars)}
{''.join(markers)}
"""
    return wrap_svg(1200, 460, body)


def main() -> int:
    save(OUT / "architecture-export.svg", build_architecture_export())
    save(OUT / "scenario-comparison.svg", build_scenario_comparison())
    save(OUT / "device-capability-matrix.svg", build_device_matrix())
    save(OUT / "baseline-timeline.svg", build_timeline("baseline_prescreen.json", "baseline timeline"))
    save(OUT / "review-timeline.svg", build_timeline("resolution_consistency_review.json", "review timeline"))
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

