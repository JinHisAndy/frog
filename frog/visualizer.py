from __future__ import annotations

import os
import sys

from .replay import build_replay
from .search import SearchResult


def launch(result: SearchResult, *, as_json: bool) -> int:
    if not result.found or result.network is None:
        print("GUI unavailable: random_search did not find a candidate. Try a larger --max-attempts.")
        return 0
    if not os.environ.get("DISPLAY") and sys.platform != "win32":
        print("GUI unavailable in this headless environment. Use `python -m frog replay --seed ... --json` instead.")
        return 0
    try:
        import tkinter as tk
    except ImportError:
        print("GUI unavailable because tkinter is not installed. Use `python -m frog replay --seed ... --json` instead.")
        return 0

    frames = build_replay(result)
    root = tk.Tk()
    root.title("Frog Python random_search replay")
    canvas = tk.Canvas(root, width=960, height=600, bg="#141823")
    canvas.pack(fill="both", expand=True)
    status = tk.StringVar(value="Ready")
    tk.Label(root, textvariable=status, anchor="w").pack(fill="x")
    current = {"index": 0}

    def draw() -> None:
        frame = frames[current["index"]]
        canvas.delete("all")
        nodes = frame.network["nodes"]
        links = frame.network["links"]
        positions: dict[str, tuple[int, int]] = {}
        layer_rows = {0: 80, 1: 300, 2: 520}
        per_layer: dict[int, int] = {}
        for node in nodes:
            layer = int(node["layer"])
            ordinal = per_layer.get(layer, 0)
            per_layer[layer] = ordinal + 1
            positions[str(node["id"])] = (90 + ordinal * 145, layer_rows[layer])
        for link in links:
            source, target = positions[str(link["source"])], positions[str(link["target"])]
            color = "#67e8f9" if float(link["weight"]) > 0 else "#64748b"
            canvas.create_line(*source, *target, fill=color, width=2)
        for node in nodes:
            x, y = positions[str(node["id"])]
            active = bool(node["activated"])
            canvas.create_oval(x - 28, y - 28, x + 28, y + 28, fill="#22c55e" if active else "#334155", outline="white")
            canvas.create_text(x, y, text=str(node["id"]), fill="white")
        status.set(f"{frame.index + 1}/{len(frames)} {frame.message}")

    def step(delta: int) -> None:
        current["index"] = max(0, min(len(frames) - 1, current["index"] + delta))
        draw()

    controls = tk.Frame(root)
    controls.pack(fill="x")
    tk.Button(controls, text="Previous", command=lambda: step(-1)).pack(side="left")
    tk.Button(controls, text="Next", command=lambda: step(1)).pack(side="left")
    draw()
    root.mainloop()
    return 0
