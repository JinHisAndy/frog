from frog.model import Chemical, Link, Node
from frog.model import Observation
from frog.network import BITE, FLEE, Network
from frog.search import SearchConfig, find_candidate


def test_same_seed_produces_same_search_result():
    first = find_candidate(SearchConfig(seed=123, max_attempts=5_000))
    second = find_candidate(SearchConfig(seed=123, max_attempts=5_000))

    assert first.to_dict() == second.to_dict()


def test_search_config_rejects_non_positive_attempt_budget():
    try:
        SearchConfig(seed=123, max_attempts=0)
    except ValueError as error:
        assert "greater than zero" in str(error)
    else:
        raise AssertionError("non-positive attempt budgets must be rejected")


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
            "dopamine_relay": Node("dopamine_relay", threshold=1, chemical=Chemical.DOPAMINE, layer=1),
            "gaba_relay": Node("gaba_relay", threshold=1, chemical=Chemical.GABA, layer=1),
        },
        links=[
            Link("input", "dopamine_relay", 95, Chemical.DOPAMINE, 20),
            Link("input", "gaba_relay", 5, Chemical.GABA, 20),
        ],
    )

    network.apply_plasticity({Chemical.DOPAMINE})

    assert network.links[0].weight == 100
    assert network.links[1].weight == 5


def test_layered_network_propagates_each_source_layer_once():
    network = Network(
        nodes={
            "pixel_a": Node("pixel_a", threshold=10, layer=0),
            "pixel_b": Node("pixel_b", threshold=10, layer=0),
            "pixel_c": Node("pixel_c", threshold=10, layer=0),
            "pixel_d": Node("pixel_d", threshold=10, layer=0),
            "pain": Node("pain", threshold=10, layer=0),
            "sweet": Node("sweet", threshold=10, layer=0),
            "relay": Node("relay", threshold=50, layer=1),
            FLEE: Node(FLEE, threshold=150, layer=2),
            BITE: Node(BITE, threshold=50, layer=2),
        },
        links=[
            Link("pixel_a", "relay", 100),
            Link("pixel_a", FLEE, 100),
            Link("relay", BITE, 100),
        ],
    )

    action = network.forward(Observation((True, False, False, False)), learn=False)

    assert action.flee is False
    assert action.bite is True


def test_network_rejects_backward_or_same_layer_links():
    try:
        Network(
            nodes={
                "input": Node("input", threshold=1, layer=0),
                "relay": Node("relay", threshold=1, layer=1),
            },
            links=[Link("relay", "input", 10)],
        )
    except ValueError as error:
        assert "forward" in str(error)
    else:
        raise AssertionError("backward links must be rejected")
