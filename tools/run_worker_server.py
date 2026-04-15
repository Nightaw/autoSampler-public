from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app


def main() -> int:
    app = create_app()
    app.run(host="127.0.0.1", port=7777, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

