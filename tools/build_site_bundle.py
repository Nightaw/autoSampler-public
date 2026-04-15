from __future__ import annotations

from html import escape
import json
import re
import shutil
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.prescreen_runner import (
    build_artifact_manifest,
    build_artifact_schema,
    build_scenario_template_manifest,
    build_showcase_manifest,
    load_json,
)
from tools.build_interview_brief import build_markdown as build_interview_markdown
from tools.build_showcase_page import build_html


SITE = ROOT / "site"


def inline_code(text: str) -> str:
    parts = text.split("`")
    chunks = []
    for index, part in enumerate(parts):
        if index % 2 == 1:
            chunks.append(f"<code>{escape(part)}</code>")
        else:
            chunks.append(escape(part))
    return "".join(chunks)


def markdown_to_html(markdown: str, title: str) -> str:
    lines = markdown.splitlines()
    html_lines: list[str] = []
    in_ul = False
    in_ol = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            html_lines.append(f"<p>{inline_code(' '.join(item.strip() for item in paragraph))}</p>")
            paragraph = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    for raw in lines:
        line = raw.rstrip()
        if not line:
            flush_paragraph()
            close_lists()
            continue
        if line.startswith("# "):
            flush_paragraph()
            close_lists()
            html_lines.append(f"<h1>{inline_code(line[2:])}</h1>")
            continue
        if line.startswith("## "):
            flush_paragraph()
            close_lists()
            html_lines.append(f"<h2>{inline_code(line[3:])}</h2>")
            continue
        if line.startswith("### "):
            flush_paragraph()
            close_lists()
            html_lines.append(f"<h3>{inline_code(line[4:])}</h3>")
            continue
        if line.startswith("- "):
            flush_paragraph()
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(f"<li>{inline_code(line[2:])}</li>")
            continue
        if re.match(r"^\d+\.\s", line):
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            stripped = re.sub(r"^\d+\.\s+", "", line)
            html_lines.append(f"<li>{inline_code(stripped)}</li>")
            continue
        paragraph.append(line)

    flush_paragraph()
    close_lists()

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Space+Grotesk:wght@400;500;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="./showcase.css" />
    <style>
      body {{ background: #f5f0e6; color: #1b1f20; font-family: "Space Grotesk", sans-serif; margin: 0; }}
      main {{ max-width: 920px; margin: 0 auto; padding: 4rem 1.25rem 5rem; }}
      h1, h2, h3 {{ font-family: "Instrument Serif", serif; font-weight: 400; line-height: 0.98; }}
      h1 {{ font-size: clamp(2.8rem, 7vw, 5rem); }}
      h2 {{ margin-top: 2.4rem; font-size: 2rem; }}
      h3 {{ margin-top: 1.8rem; font-size: 1.4rem; }}
      p, li {{ color: #4f544f; line-height: 1.7; font-size: 1rem; }}
      ul, ol {{ padding-left: 1.25rem; }}
      code {{ background: rgba(24, 58, 55, 0.08); padding: 0.12rem 0.35rem; border-radius: 0.35rem; }}
      .back {{ display: inline-block; margin-bottom: 2rem; color: #476c9b; }}
    </style>
  </head>
  <body>
    <main>
      <a class="back" href="./index.html">Back to showcase</a>
      {''.join(html_lines)}
    </main>
  </body>
</html>"""


def rewrite_showcase_for_site(html: str) -> str:
    replacements = {
        "../README.md": "https://github.com/Nightaw/autoSampler-public",
        "../docs/architecture.md": "./documents/architecture.html",
        "../docs/interview-brief.md": "./interview-brief.html",
        "../docs/scenario-templates.json": "./data/scenario_templates.json",
        "../docs/artifact-schema.json": "./data/artifact_schema.json",
        "../docs/generated/architecture-export.svg": "./assets/generated/architecture-export.svg",
        "../docs/generated/scenario-comparison.svg": "./assets/generated/scenario-comparison.svg",
        "../docs/generated/device-capability-matrix.svg": "./assets/generated/device-capability-matrix.svg",
        "../docs/generated/baseline-timeline.svg": "./assets/generated/baseline-timeline.svg",
        "../docs/generated/review-timeline.svg": "./assets/generated/review-timeline.svg",
        "../docs/hero.svg": "./assets/hero.svg",
        "../samples/results/stall_storyboard.jpg": "./assets/results/stall_storyboard.jpg",
        "../samples/results/resolution_storyboard.jpg": "./assets/results/resolution_storyboard.jpg",
        "../samples/results/resolution_review_storyboard.jpg": "./assets/results/resolution_review_storyboard.jpg",
        "../samples/results/baseline_prescreen.json": "./data/results/baseline_prescreen.json",
        "../samples/results/resolution_consistency_review.json": "./data/results/resolution_consistency_review.json",
        "../samples/payloads/baseline_prescreen.json": "./data/payloads/baseline_prescreen.json",
        "../samples/payloads/resolution_consistency_review.json": "./data/payloads/resolution_consistency_review.json",
        "./showcase_manifest.json": "./data/showcase_manifest.json",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html


def build_case_page(
    report_name: str,
    *,
    stylesheet_href: str,
    back_href: str,
    storyboard_href: str,
    timeline_href: str,
) -> str:
    report = load_json(ROOT / "samples" / "results" / report_name)
    summary = report["summary"]
    warnings = "".join(f"<li>{escape(item)}</li>" for item in report["metrics"]["heuristic"]["warnings"])
    reasons = "".join(f"<li>{escape(item)}</li>" for item in report["metrics"]["heuristic"]["reasons"])
    steps = "".join(
        f"<li><strong>{escape(step['name'])}</strong><span>{escape(step['details'])}</span></li>"
        for step in report["execution"]["steps"]
    )
    problem_text = (
        "Demonstrate the expected pass path for a clean capture-review sample."
        if report_name == "baseline_prescreen.json"
        else "Demonstrate how a review-worthy regression is surfaced under constrained bandwidth."
    )
    evidence_text = (
        "The sample includes bounded stall windows, multiple resolution transitions, and complete visual evidence."
        if report_name == "baseline_prescreen.json"
        else "The sample includes overlapping stalls, sparse resolution transitions, and a suspiciously high final quality label."
    )
    decision_text = (
        "The heuristics return pass because timing, bandwidth hints, and resolution behavior stay internally consistent."
        if report_name == "baseline_prescreen.json"
        else "The heuristics return review because the quality trajectory conflicts with the constrained network profile."
    )
    output_text = (
        "The runner emits baseline-grade JSON, Markdown, storyboard, and timeline artifacts for downstream reuse."
        if report_name == "baseline_prescreen.json"
        else "The runner emits escalation-ready JSON, Markdown, storyboard, and timeline artifacts for manual verification."
    )
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(report['scenario']['title'])}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Space+Grotesk:wght@400;500;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="{escape(stylesheet_href)}" />
    <style>
      body {{ margin: 0; background: #f6f1e8; color: #1b1f20; font-family: "Space Grotesk", sans-serif; }}
      main {{ max-width: 1120px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
      h1, h2 {{ font-family: "Instrument Serif", serif; font-weight: 400; line-height: 0.96; }}
      h1 {{ font-size: clamp(3rem, 8vw, 5.8rem); margin: 0; max-width: 10ch; }}
      h2 {{ font-size: 2rem; margin: 0 0 1rem; }}
      p, li {{ line-height: 1.65; color: #505551; }}
      .top {{ display: grid; grid-template-columns: 1fr 0.9fr; gap: 2rem; align-items: end; }}
      .stats {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
      .stats div {{ border-top: 1px solid rgba(27,31,32,0.12); padding-top: 0.8rem; }}
      .stats span {{ display: block; color: #6a6f69; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.12em; }}
      .stats strong {{ display: block; margin-top: 0.4rem; font-size: 1.45rem; }}
      .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.5rem; margin-top: 2.5rem; }}
      .panel {{ border: 1px solid rgba(27,31,32,0.12); border-radius: 1.4rem; background: rgba(255,255,255,0.5); padding: 1.25rem; }}
      .image-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
      .image-grid img {{ border-radius: 1rem; border: 1px solid rgba(27,31,32,0.12); background: #fff; }}
      .step-list, .flag-list {{ list-style: none; padding: 0; margin: 0; }}
      .step-list li, .flag-list li {{ padding: 0.8rem 0; border-top: 1px solid rgba(27,31,32,0.1); }}
      .story-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin-top: 2rem; }}
      .story-card {{ border: 1px solid rgba(27,31,32,0.12); border-radius: 1.2rem; background: rgba(255,255,255,0.55); padding: 1rem; }}
      .story-card span {{ display: block; margin-bottom: 0.6rem; color: #6a6f69; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.14em; }}
      .back {{ display: inline-block; margin-bottom: 1rem; color: #476c9b; }}
      @media (max-width: 900px) {{ .top, .grid, .image-grid, .story-grid {{ grid-template-columns: 1fr; }} }}
    </style>
  </head>
  <body>
    <main>
      <a class="back" href="{escape(back_href)}">Back to showcase</a>
      <section class="top">
        <div>
          <p class="eyebrow">{escape(report['scenario']['execution_profile'])}</p>
          <h1>{escape(report['scenario']['title'])}</h1>
          <p>{escape(report['scenario']['description'])}</p>
        </div>
        <div class="stats">
          <div><span>Decision</span><strong>{escape(str(summary['final_decision']).upper())}</strong></div>
          <div><span>Score</span><strong>{escape(str(summary['final_score']))}</strong></div>
          <div><span>Stalls</span><strong>{escape(str(summary['stall_count']))}</strong></div>
          <div><span>Resolution events</span><strong>{escape(str(summary['resolution_count']))}</strong></div>
        </div>
      </section>
      <section class="story-grid">
        <article class="story-card"><span>Problem</span><p>{escape(problem_text)}</p></article>
        <article class="story-card"><span>Evidence</span><p>{escape(evidence_text)}</p></article>
        <article class="story-card"><span>Decision</span><p>{escape(decision_text)}</p></article>
        <article class="story-card"><span>Output</span><p>{escape(output_text)}</p></article>
      </section>
      <section class="grid">
        <article class="panel">
          <h2>Scenario summary</h2>
          <p>Unit id: <code>{escape(summary['unit_id'])}</code></p>
          <p>Bandwidth: <code>{escape(str(summary['bandwidth_kbps']))} kbps</code></p>
          <p>Work duration: <code>{escape(str(summary['work_duration_seconds']))}s</code></p>
          <p>Device target: <code>{escape(report['devices'][0]['device_id'])}</code></p>
        </article>
        <article class="panel">
          <h2>Execution plan</h2>
          <p>Profile: <code>{escape(report['execution']['profile'])}</code></p>
          <p>Focus: <code>{escape(', '.join(report['metrics']['execution_plan']['focus']))}</code></p>
          <p>Ordered steps: <code>{escape(' -> '.join(report['metrics']['execution_plan']['steps']))}</code></p>
        </article>
      </section>
      <section class="grid">
        <article class="panel">
          <h2>Evidence assets</h2>
          <div class="image-grid">
            <img src="{escape(storyboard_href)}" alt="storyboard one" />
            <img src="{escape(timeline_href)}" alt="timeline export" />
          </div>
        </article>
        <article class="panel">
          <h2>Execution trace</h2>
          <ul class="step-list">{steps}</ul>
        </article>
      </section>
      <section class="grid">
        <article class="panel">
          <h2>Warnings</h2>
          <ul class="flag-list">{warnings or '<li>No warnings in this scenario.</li>'}</ul>
        </article>
        <article class="panel">
          <h2>Reasons</h2>
          <ul class="flag-list">{reasons or '<li>No hard rejection reasons were triggered.</li>'}</ul>
        </article>
      </section>
    </main>
  </body>
</html>"""


def copy_tree(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    shutil.copytree(src, dst)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True, exist_ok=True)

    copy_file(ROOT / "docs" / "showcase.css", SITE / "showcase.css")
    copy_file(ROOT / "docs" / "hero.svg", SITE / "assets" / "hero.svg")
    copy_tree(ROOT / "docs" / "generated", SITE / "assets" / "generated")
    copy_tree(ROOT / "samples" / "results", SITE / "assets" / "results")
    copy_tree(ROOT / "samples" / "payloads", SITE / "data" / "payloads")
    copy_tree(ROOT / "samples" / "results", SITE / "data" / "results")

    architecture_html = markdown_to_html((ROOT / "docs" / "architecture.md").read_text(encoding="utf-8"), "Architecture")
    design_html = markdown_to_html((ROOT / "docs" / "design-decisions.md").read_text(encoding="utf-8"), "Design Decisions")
    interview_html = markdown_to_html(build_interview_markdown(), "Interview Brief")

    (SITE / "documents").mkdir(parents=True, exist_ok=True)
    (SITE / "documents" / "architecture.html").write_text(architecture_html, encoding="utf-8")
    (SITE / "documents" / "design-decisions.html").write_text(design_html, encoding="utf-8")
    (SITE / "interview-brief.html").write_text(interview_html, encoding="utf-8")

    manifest = build_showcase_manifest()
    artifact_manifest = build_artifact_manifest()
    template_manifest = build_scenario_template_manifest()
    artifact_schema = build_artifact_schema()
    (SITE / "data" / "showcase_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (SITE / "data" / "artifact_manifest.json").write_text(json.dumps(artifact_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (SITE / "data" / "scenario_templates.json").write_text(json.dumps(template_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (SITE / "data" / "artifact_schema.json").write_text(json.dumps(artifact_schema, indent=2, ensure_ascii=False), encoding="utf-8")

    (SITE / "index.html").write_text(rewrite_showcase_for_site(build_html()), encoding="utf-8")
    (SITE / "cases").mkdir(parents=True, exist_ok=True)
    (SITE / "cases" / "baseline_prescreen.html").write_text(
        build_case_page(
            "baseline_prescreen.json",
            stylesheet_href="../showcase.css",
            back_href="../index.html",
            storyboard_href="../assets/results/stall_storyboard.jpg",
            timeline_href="../assets/generated/baseline-timeline.svg",
        ),
        encoding="utf-8",
    )
    (SITE / "cases" / "resolution_consistency_review.html").write_text(
        build_case_page(
            "resolution_consistency_review.json",
            stylesheet_href="../showcase.css",
            back_href="../index.html",
            storyboard_href="../assets/results/resolution_review_storyboard.jpg",
            timeline_href="../assets/generated/review-timeline.svg",
        ),
        encoding="utf-8",
    )
    print(SITE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
