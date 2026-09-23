from __future__ import annotations

import argparse
import json
from typing import Sequence

from .replay import build_replay
from .search import SearchConfig, find_candidate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m frog",
        description="Deterministic, inspectable random-network search prototype.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    for name in ("search", "replay", "gui"):
        command = subcommands.add_parser(name)
        command.add_argument("--seed", type=int, required=True)
        command.add_argument("--max-attempts", type=int, default=50_000)
        command.add_argument("--json", action="store_true", dest="as_json")
    return parser


def _result(args: argparse.Namespace):
    return find_candidate(SearchConfig(seed=args.seed, max_attempts=args.max_attempts))


def run(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    result = _result(args)

    if args.command == "search":
        payload = result.to_dict()
    elif args.command == "replay":
        payload = result.to_dict()
        payload["frames"] = [frame.to_dict() for frame in build_replay(result)]
    else:
        from .visualizer import launch

        return launch(result, as_json=args.as_json)

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    elif result.found:
        print(f"random_search found a candidate after {result.attempts} attempts (seed={result.seed}).")
        print(json.dumps(result.blind_test, ensure_ascii=False, indent=2))
    else:
        print(f"random_search found no candidate in {result.attempts} attempts (seed={result.seed}).")
    return 0
