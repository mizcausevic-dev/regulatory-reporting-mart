from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.mart_builder import write_site


if __name__ == "__main__":
    root = write_site()
    required = [
        root / "index.html",
        root / "reporting-lane" / "index.html",
        root / "deadline-pressure" / "index.html",
        root / "evidence-posture" / "index.html",
        root / "verification" / "index.html",
        root / "docs" / "index.html",
        root / "robots.txt",
        root / "sitemap.xml",
        root / "api" / "dashboard.json",
    ]
    missing = [str(path) for path in required if not Path(path).is_file()]
    if missing:
        raise SystemExit("Missing generated assets: " + ", ".join(missing))
    print("Smoke check passed for", root)
