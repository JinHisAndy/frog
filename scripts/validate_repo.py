from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PATTERNS = ("*.java", "pom.xml", "run.bat", "run.sh", "maven_*.bat")


def main() -> int:
    offenders: list[Path] = []
    for pattern in FORBIDDEN_PATTERNS:
        offenders.extend(path for path in ROOT.rglob(pattern) if ".git" not in path.parts)
    if offenders:
        print("legacy executable residue found:")
        for path in sorted(set(offenders)):
            print(path.relative_to(ROOT))
        return 1
    command = [sys.executable, "-m", "pytest", "-q"]
    return subprocess.run(command, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
