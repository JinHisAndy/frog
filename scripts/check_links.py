from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)#]+)(?:#[^)]+)?\)")


def main() -> int:
    broken: list[tuple[Path, str]] = []
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts or "archive" in markdown.relative_to(ROOT).parts:
            continue
        text = markdown.read_text(encoding="utf-8-sig", errors="replace")
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            destination = (markdown.parent / target).resolve()
            if not destination.exists():
                broken.append((markdown.relative_to(ROOT), target))
    if broken:
        print("broken local markdown links:")
        for markdown, target in broken:
            print(f"{markdown}: {target}")
        return 1
    print("local markdown links: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
