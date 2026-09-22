import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENGINE_DIR = ROOT / "study_question_engine_FINAL_v1_0" / "study_question_engine_final"
MAIN = ENGINE_DIR / "main.py"

if not MAIN.exists():
    raise SystemExit(f"Engine not found: {MAIN}")

args = sys.argv[1:]
if args and args[0] == "import-json" and len(args) >= 2:
    raw = Path(args[1])
    if not raw.is_absolute():
        candidates = [ROOT / raw, ENGINE_DIR / raw]
        for candidate in candidates:
            if candidate.exists():
                args[1] = str(candidate)
                break

cmd = [sys.executable, str(MAIN), *args]
raise SystemExit(subprocess.call(cmd, cwd=str(ENGINE_DIR)))
