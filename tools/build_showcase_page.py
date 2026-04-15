from __future__ import annotations

from html import escape
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from common.prescreen_runner import build_showcase_manifest


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def rel(path: str) -> str:
    return "../" + path


def count_tests() -> int:
    total = 0
    for path in (ROOT / "tests").glob("test_*.py"):
        total += path.read_text(encoding="utf-8").count("def test_")
    return total


def scenario_markup(scenario: dict) -> str:
    summary = scenario.get("summary") or {}
    decision = escape(str(summary.get("final_decision", "n/a")).upper())
    decision_class = decision.lower()
    focus = "".join(f"<li>{escape(item)}</li>" for item in scenario.get("focus", []))
    return f"""
    <article class="scenario-block {decision_class}">
      <div class="scenario-head">
        <p class="eyebrow">{escape(scenario.get("execution_profile", ""))}</p>
        <span class="decision {decision_class}">{decision}</span>
      </div>
      <h3>{escape(scenario.get("title", ""))}</h3>
      <p class="scenario-copy">{escape(scenario.get("description", ""))}</p>
      <dl class="metric-grid">
        <div><dt>Score</dt><dd>{escape(str(summary.get("final_score", "-")))}</dd></div>
        <div><dt>Bandwidth</dt><dd>{escape(str(summary.get("bandwidth_kbps", "-")))} kbps</dd></div>
        <div><dt>Stalls</dt><dd>{escape(str(summary.get("stall_count", "-")))}</dd></div>
        <div><dt>Resolution events</dt><dd>{escape(str(summary.get("resolution_count", "-")))}</dd></div>
      </dl>
      <ul class="focus-list">{focus}</ul>
      <div class="scenario-links">
        <a href="{escape(rel(scenario.get("payload", "")))}">payload</a>
        <a href="{escape(rel(scenario.get("result", "")))}">result</a>
      </div>
    </article>
    """


def build_html() -> str:
    manifest = build_showcase_manifest()
    baseline = load_json(ROOT / "samples" / "results" / "baseline_prescreen.json")
    review = load_json(ROOT / "samples" / "results" / "resolution_consistency_review.json")
    test_count = count_tests()

    scenarios = "\n".join(scenario_markup(item) for item in manifest["scenarios"])
    architecture_steps = "".join(
        f"<li><span>{index:02d}</span><p>{escape(step)}</p></li>"
        for index, step in enumerate(
            [
                "Sample unit enters the queue with description metadata and screen recording.",
                "Device registry resolves a capture target and execution profile.",
                "Scenario planner expands worker steps into a deterministic run plan.",
                "Heuristic scorer validates stall and resolution labels against timing and bandwidth.",
                "Storyboard generator exports reviewer-friendly image evidence.",
                "JSON and Markdown artifacts are returned through CLI and API surfaces.",
            ],
            start=1,
        )
    )
    api_routes = "".join(
        f"<li><code>{escape(route)}</code></li>"
        for route in [
            "GET /demo/devices",
            "GET /demo/scenarios",
            "GET /demo/scenarios/<scenario_name>",
            "GET /demo/showcase",
            "POST /demo/run",
            "POST /demo/jobs",
            "POST /demo/jobs/process",
        ]
    )
    baseline_steps = "".join(
        f"<li><strong>{escape(step['name'])}</strong><span>{escape(step['details'])}</span></li>"
        for step in baseline["execution"]["steps"]
    )
    review_warnings = "".join(
        f"<li>{escape(item)}</li>" for item in review["metrics"]["heuristic"]["warnings"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>autoSampler Public Showcase</title>
    <meta
      name="description"
      content="Worker-style media label prescreen demo with device selection, scenario planning, storyboard evidence, and structured reporting."
    />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Space+Grotesk:wght@400;500;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="./showcase.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="hero">
        <nav class="topbar">
          <span class="brand">autoSampler Public</span>
          <div class="toplinks">
            <a href="../README.md">README</a>
            <a href="./showcase_manifest.json">manifest</a>
            <a href="https://github.com/Nightaw/autoSampler-public">GitHub</a>
          </div>
        </nav>
        <div class="hero-grid">
          <div class="hero-copy reveal">
            <p class="eyebrow">worker-style media quality review</p>
            <h1>Post-capture sampling turned into a portfolio-grade service demo.</h1>
            <p class="lede">
              Sample-unit ingestion, device selection, execution planning, heuristic label review,
              storyboard evidence, and structured artifacts are organized into a compact public system.
            </p>
            <div class="cta-row">
              <a class="primary" href="../samples/results/baseline_prescreen.json">Open baseline report</a>
              <a class="secondary" href="../docs/architecture.md">Read architecture</a>
              <a class="secondary" href="../docs/interview-brief.md">Interview brief</a>
            </div>
          </div>
          <div class="hero-visual reveal">
            <div class="poster-frame poster-a">
              <img src="../samples/results/stall_storyboard.jpg" alt="stall storyboard" />
            </div>
            <div class="poster-frame poster-b">
              <img src="../samples/results/resolution_review_storyboard.jpg" alt="resolution review storyboard" />
            </div>
            <div class="signal-panel">
              <div>
                <span>Baseline</span>
                <strong>{baseline['summary']['final_score']}</strong>
                <em>{baseline['summary']['final_decision']}</em>
              </div>
              <div>
                <span>Review case</span>
                <strong>{review['summary']['final_score']}</strong>
                <em>{review['summary']['final_decision']}</em>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main>
        <section class="band reveal">
          <div>
            <p class="eyebrow">project signal</p>
            <h2>One pipeline, two outcomes, multiple surfaces.</h2>
          </div>
          <div class="band-stats">
            <div><span>Scenarios</span><strong>{len(manifest['scenarios'])}</strong></div>
            <div><span>API routes</span><strong>7</strong></div>
            <div><span>Tests</span><strong>{test_count}</strong></div>
            <div><span>Artifacts</span><strong>JSON + MD + JPG</strong></div>
          </div>
        </section>

        <section class="split-section">
          <div class="section-head reveal">
            <p class="eyebrow">system composition</p>
            <h2>Execution planning is treated as a first-class layer, not hidden inside one script.</h2>
          </div>
          <div class="arch-layout">
            <ol class="arch-track reveal">{architecture_steps}</ol>
            <div class="arch-side reveal">
              <img src="../docs/generated/architecture-export.svg" alt="project architecture export" />
              <p>
                The public repo keeps the same shape as a larger internal workflow: queue-style entry,
                execution targeting, scoring, evidence generation, and downstream artifact delivery.
              </p>
            </div>
          </div>
        </section>

        <section class="gallery-section">
          <div class="section-head reveal">
            <p class="eyebrow">generated visuals</p>
            <h2>Repository assets now export into ready-to-share diagrams instead of ad-hoc screenshots.</h2>
          </div>
          <div class="gallery-strip reveal">
            <figure>
              <img src="../docs/generated/scenario-comparison.svg" alt="scenario comparison chart" />
              <figcaption>Scenario scores and outcome split across bundled sample units.</figcaption>
            </figure>
            <figure>
              <img src="../docs/generated/device-capability-matrix.svg" alt="device capability matrix" />
              <figcaption>Mock execution targets mapped by role, platform, and worker capability.</figcaption>
            </figure>
            <figure>
              <img src="../docs/generated/baseline-timeline.svg" alt="baseline timeline chart" />
              <figcaption>Timeline export for stall windows and resolution transitions.</figcaption>
            </figure>
          </div>
        </section>

        <section class="scenario-section">
          <div class="section-head reveal">
            <p class="eyebrow">scenarios</p>
            <h2>Two sample units show both a clean pass path and a review-worthy edge case.</h2>
          </div>
          <div class="scenario-grid">{scenarios}</div>
        </section>

        <section class="gallery-section">
          <div class="section-head reveal">
            <p class="eyebrow">evidence surface</p>
            <h2>Storyboard artifacts make the review path legible in seconds.</h2>
          </div>
          <div class="gallery-strip reveal">
            <figure>
              <img src="../samples/results/stall_storyboard.jpg" alt="stall storyboard" />
              <figcaption>Stall evidence extracted from the baseline unit.</figcaption>
            </figure>
            <figure>
              <img src="../samples/results/resolution_storyboard.jpg" alt="resolution storyboard" />
              <figcaption>Resolution transitions from the baseline scenario.</figcaption>
            </figure>
            <figure>
              <img src="../samples/results/resolution_review_storyboard.jpg" alt="resolution review storyboard" />
              <figcaption>Review case with sparse quality transitions under limited bandwidth.</figcaption>
            </figure>
          </div>
        </section>

        <section class="detail-grid">
          <article class="detail-panel reveal">
            <p class="eyebrow">baseline execution trace</p>
            <h2>Worker steps are persisted as structured evidence.</h2>
            <ul class="trace-list">{baseline_steps}</ul>
          </article>
          <article class="detail-panel accent reveal">
            <p class="eyebrow">review findings</p>
            <h2>The second case demonstrates why this is more than a happy-path demo.</h2>
            <ul class="warning-list">{review_warnings}</ul>
          </article>
        </section>

        <section class="gallery-section">
          <div class="section-head reveal">
            <p class="eyebrow">timeline exports</p>
            <h2>Two timeline views make the baseline and review cases comparable at a glance.</h2>
          </div>
          <div class="gallery-strip reveal">
            <figure>
              <img src="../docs/generated/baseline-timeline.svg" alt="baseline timeline export" />
              <figcaption>Baseline run with multiple resolution events and bounded stall windows.</figcaption>
            </figure>
            <figure>
              <img src="../docs/generated/review-timeline.svg" alt="review timeline export" />
              <figcaption>Review run with overlapping stalls and sparse resolution changes.</figcaption>
            </figure>
            <figure>
              <img src="../docs/hero.svg" alt="project hero diagram" />
              <figcaption>Compact hero asset for README, slides, or portfolio previews.</figcaption>
            </figure>
          </div>
        </section>

        <section class="api-section">
          <div class="section-head reveal">
            <p class="eyebrow">service surface</p>
            <h2>The same demo is exposed through CLI, queue simulation, and API endpoints.</h2>
          </div>
          <div class="api-layout">
            <ul class="route-list reveal">{api_routes}</ul>
            <div class="terminal reveal">
<pre><code>python3 tools/run_worker_server.py
curl -X POST http://127.0.0.1:7777/demo/run \\
  -H "Content-Type: application/json" \\
  -d @samples/payloads/baseline_prescreen.json

python3 tools/export_showcase_bundle.py
python3 tools/build_showcase_page.py</code></pre>
            </div>
          </div>
        </section>

        <section class="bilingual-section reveal">
          <div>
            <p class="eyebrow">english</p>
            <p>
              autoSampler-public is a compact worker-style demo for post-capture media quality review,
              covering sample ingestion, device selection, scenario planning, heuristic validation,
              storyboard evidence, and structured report delivery.
            </p>
          </div>
          <div>
            <p class="eyebrow">中文</p>
            <p>
              autoSampler-public 是一个面向采样后处理链路的轻量公开演示项目，覆盖 sample unit 读取、
              设备选择、场景执行规划、标签规则校验、storyboard 证据生成，以及结构化报告输出。
            </p>
          </div>
        </section>

        <section class="band reveal">
          <div>
            <p class="eyebrow">interview mode</p>
            <h2>Slides, brief, diagrams, reports, and static page are all generated from the same repo state.</h2>
          </div>
          <div class="band-stats">
            <div><span>Brief</span><strong><a href="../docs/interview-brief.md">interview-brief.md</a></strong></div>
            <div><span>Visual exports</span><strong>5 SVG</strong></div>
            <div><span>Showcase page</span><strong><a href="../docs/index.html">docs/index.html</a></strong></div>
            <div><span>Manifest</span><strong><a href="../docs/showcase_manifest.json">JSON</a></strong></div>
          </div>
        </section>
      </main>
    </div>

    <script>
      const observer = new IntersectionObserver((entries) => {{
        for (const entry of entries) {{
          if (entry.isIntersecting) {{
            entry.target.classList.add("is-visible");
          }}
        }}
      }}, {{ threshold: 0.16 }});

      document.querySelectorAll(".reveal").forEach((node) => observer.observe(node));
      document.querySelectorAll(".poster-frame").forEach((node, index) => {{
        node.style.transform = `translateY(${{index * 14}}px) rotate(${{index === 0 ? -3 : 4}}deg)`;
      }});
    </script>
  </body>
</html>
"""


def main() -> int:
    output_path = ROOT / "docs" / "index.html"
    output_path.write_text(build_html(), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
