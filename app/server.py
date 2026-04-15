from __future__ import annotations

from flask import Flask, jsonify, request

from common.device_registry import list_devices
from common.job_queue import enqueue_job, get_job, list_jobs, process_next_job
from common.prescreen_runner import (
    build_artifact_manifest,
    build_artifact_schema,
    build_markdown_report,
    build_scenario_template_manifest,
    build_showcase_manifest,
    describe_architecture,
    get_scenario,
    list_scenarios,
    run_demo_scenario,
)


def register_routes(app: Flask) -> None:
    @app.get("/health")
    def health() -> tuple[str, int]:
        return "ok", 200

    @app.get("/demo/scenarios")
    def scenarios():
        return jsonify({"scenarios": list_scenarios()})

    @app.get("/demo/scenarios/<scenario_name>")
    def scenario_detail(scenario_name: str):
        return jsonify(get_scenario(scenario_name))

    @app.get("/demo/devices")
    def devices():
        platform = request.args.get("platform")
        role = request.args.get("role")
        return jsonify({"devices": list_devices(platform=platform, role=role)})

    @app.get("/demo/architecture")
    def architecture():
        return jsonify(describe_architecture())

    @app.get("/demo/showcase")
    def showcase():
        return jsonify(build_showcase_manifest())

    @app.get("/demo/artifacts")
    def artifacts():
        return jsonify(build_artifact_manifest())

    @app.get("/demo/templates")
    def templates():
        return jsonify(build_scenario_template_manifest())

    @app.get("/demo/schemas")
    def schemas():
        return jsonify({"artifact_manifest": build_artifact_schema()})

    @app.get("/demo/jobs")
    def jobs():
        return jsonify({"jobs": list_jobs()})

    @app.get("/demo/jobs/<job_id>")
    def job_detail(job_id: str):
        job = get_job(job_id)
        if not job:
            return jsonify({"error": "job not found"}), 404
        return jsonify(job)

    @app.post("/demo/jobs")
    def create_job():
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "baseline_prescreen")
        return jsonify(enqueue_job(scenario)), 201

    @app.post("/demo/jobs/process")
    def process_job():
        job = process_next_job()
        if job is None:
            return jsonify({"error": "no queued jobs"}), 404
        return jsonify(job)

    @app.post("/demo/run")
    def run_demo():
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "baseline_prescreen")
        report = run_demo_scenario(scenario)
        return jsonify(report)

    @app.get("/demo/report.md")
    def markdown_report():
        scenario = request.args.get("scenario", "baseline_prescreen")
        return build_markdown_report(scenario), 200, {"Content-Type": "text/markdown; charset=utf-8"}
