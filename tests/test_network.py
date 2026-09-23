from frog.model import Chemical, Link, Node
from frog.network import Network
from frog.search import SearchConfig, find_candidate


def test_same_seed_produces_same_search_result():
    first = find_candidate(SearchConfig(seed=123, max_attempts=5_000))
    second = find_candidate(SearchConfig(seed=123, max_attempts=5_000))

    assert first.to_dict() == second.to_dict()


def test_found_candidate_passes_blind_enemy_food_and_noise_cases():
    result = find_candidate(SearchConfig(seed=123, max_attempts=50_000))

    assert result.found
    assert result.blind_test == {
        "enemy": {"flee": True, "bite": False},
        "food": {"flee": False, "bite": True},
        "noise": {"flee": False, "bite": False},
    }
    assert result.blind_inputs == {
        "enemy": {"pixels": [True, True, False, False], "pain": False, "sweet": False},
        "food": {"pixels": [False, True, True, True], "pain": False, "sweet": False},
        "noise": {"pixels": [False, False, False, True], "pain": False, "sweet": False},
    }


def test_plasticity_only_changes_links_for_active_chemical_and_clamps_weight():
    network = Network(
        nodes={
            "input": Node("input", threshold=1),
            "dopamine_relay": Node("dopamine_relay", threshold=1, chemical=Chemical.DOPAMINE),
            "gaba_relay": Node("gaba_relay", threshold=1, chemical=Chemical.GABA),
        },
        links=[
            Link("input", "dopamine_relay", 95, Chemical.DOPAMINE, 20),
            Link("input", "gaba_relay", 5, Chemical.GABA, 20),
        ],
    )

    network.apply_plasticity({Chemical.DOPAMINE})

    assert network.links[0].weight == 100
    assert network.links[1].weight == 5
