import json
import subprocess
import sys

from frog.replay import build_replay
from frog.search import SearchConfig, find_candidate


def test_replay_frames_are_ordered_and_include_blind_frames():
    result = find_candidate(SearchConfig(seed=123, max_attempts=50_000))
    frames = build_replay(result)

    assert [frame.index for frame in frames] == list(range(len(frames)))
    assert {frame.phase for frame in frames} >= {"blind_enemy", "blind_food", "blind_noise"}
    assert frames[-1].action is not None


def test_replay_uses_the_trace_captured_during_search_without_retraining():
    result = find_candidate(SearchConfig(seed=123, max_attempts=50_000))

    assert result.training_trace
    frames = build_replay(result)

    assert frames[: len(result.training_trace)] == result.training_trace


def test_search_cli_emits_parseable_random_search_evidence():
    completed = subprocess.run(
        [sys.executable, "-m", "frog", "search", "--seed", "123", "--max-attempts", "50000", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["method"] == "random_search"
    assert payload["found"] is True
    assert payload["blind_test"]["noise"] == {"flee": False, "bite": False}
