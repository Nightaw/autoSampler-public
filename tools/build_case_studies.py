from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_site_bundle import build_case_page


def main() -> int:
    cases_dir = ROOT / "docs" / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)
    (cases_dir / "baseline_prescreen.html").write_text(
        build_case_page(
            "baseline_prescreen.json",
            stylesheet_href="../showcase.css",
            back_href="../index.html",
            storyboard_href="../../samples/results/stall_storyboard.jpg",
            timeline_href="../generated/baseline-timeline.svg",
        ),
        encoding="utf-8",
    )
    (cases_dir / "resolution_consistency_review.html").write_text(
        build_case_page(
            "resolution_consistency_review.json",
            stylesheet_href="../showcase.css",
            back_href="../index.html",
            storyboard_href="../../samples/results/resolution_review_storyboard.jpg",
            timeline_href="../generated/review-timeline.svg",
        ),
        encoding="utf-8",
    )
    print(cases_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
