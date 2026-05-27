from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.mart_builder import write_site


if __name__ == "__main__":
    root = write_site()
    print(root)
