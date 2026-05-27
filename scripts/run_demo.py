from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.mart_builder import build_dashboard


if __name__ == "__main__":
    dashboard = build_dashboard()
    print("Generated:", dashboard["generated_on"])
    print("Dockets:", dashboard["docket_count"])
    print("Average readiness:", dashboard["avg_readiness"])
    print("Max late risk:", dashboard["max_late_risk"])
