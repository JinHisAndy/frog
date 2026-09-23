from __future__ import annotations

import random
from dataclasses import dataclass

from .model import Chemical, Frame, Link, Node, Observation
from .network import BITE, FLEE, INPUT_NAMES, Network

ENEMY = Observation((True, True, False, False), pain=False, sweet=False)
FOOD = Observation((False, True, True, True), pain=False, sweet=False)
NOISE = Observation((False, False, False, True), pain=False, sweet=False)
TRAIN_ENEMY = Observation((True, True, False, False), pain=True, sweet=False)
TRAIN_FOOD = Observation((False, True, True, True), pain=False, sweet=True)


@dataclass(frozen=True)
class SearchConfig:
    seed: int
    max_attempts: int = 50_000

    def __post_init__(self) -> None:
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be greater than zero")


@dataclass
class SearchResult:
    seed: int
    attempts: int
    found: bool
    network: Network | None
    blind_test: dict[str, dict[str, bool]]
    blind_inputs: dict[str, dict[str, object]]
    training_trace: list[Frame]
    method: str = "random_search"

    def to_dict(self) -> dict[str, object]:
        return {
            "method": self.method,
            "seed": self.seed,
            "attempts": self.attempts,
            "found": self.found,
            "network": self.network.to_dict() if self.network else None,
            "blind_test": self.blind_test,
            "blind_inputs": self.blind_inputs,
            "training_trace": [frame.to_dict() for frame in self.training_trace],
        }


def _candidate(random_source: random.Random) -> Network:
    nodes: dict[str, Node] = {
        name: Node(name, threshold=10.0, layer=0) for name in INPUT_NAMES
    }
    chemicals = [Chemical.DOPAMINE, Chemical.NOREPINEPHRINE, Chemical.GLUTAMATE, Chemical.GABA]
    for index in range(6):
        name = f"relay_{index + 1}"
        nodes[name] = Node(
            name,
            threshold=float(random_source.choice((50, 100, 150, 200))),
            chemical=random_source.choice(chemicals),
            layer=1,
        )
    nodes[FLEE] = Node(FLEE, threshold=50.0, layer=2)
    nodes[BITE] = Node(BITE, threshold=50.0, layer=2)

    sources = list(nodes)
    links: list[Link] = []
    for _ in range(random_source.randint(22, 33)):
        source = random_source.choice(sources)
        targets = [
            identifier
            for identifier, node in nodes.items()
            if nodes[source].layer < node.layer
        ]
        if not targets:
            continue
        target = random_source.choice(targets)
        links.append(
            Link(
                source=source,
                target=target,
                weight=float(random_source.choice((0, 25, 50, 75, 100))),
                modulated_by=random_source.choice(chemicals + [Chemical.NONE]),
                plasticity_delta=float(random_source.choice((-25, 0, 25))),
            )
        )
    return Network(nodes=nodes, links=links)


def _blind_test(network: Network) -> tuple[dict[str, dict[str, bool]], dict[str, dict[str, object]]]:
    scenarios = blind_observations()
    outcomes: dict[str, dict[str, bool]] = {}
    inputs: dict[str, dict[str, object]] = {}
    for name, observation in scenarios.items():
        action = network.forward(observation, learn=False)
        outcomes[name] = action.to_dict()
        inputs[name] = observation.to_dict()
    return outcomes, inputs


def _passes(outcomes: dict[str, dict[str, bool]]) -> bool:
    return outcomes == {
        "enemy": {"flee": True, "bite": False},
        "food": {"flee": False, "bite": True},
        "noise": {"flee": False, "bite": False},
    }


def _train(network: Network, label: str, observation: Observation, index: int) -> list[Frame]:
    before = Frame(
        index=index,
        phase=label,
        message=f"{label}: captured immediately before the real training step",
        observation=observation,
        network=network.to_dict(),
    )
    action = network.forward(observation, learn=True)
    after = Frame(
        index=index + 1,
        phase=label,
        message=f"{label}: captured immediately after the real training step",
        observation=observation,
        active_chemicals=sorted(network.active_chemicals(), key=str),
        action=action,
        network=network.to_dict(),
    )
    return [before, after]


def find_candidate(config: SearchConfig) -> SearchResult:
    random_source = random.Random(config.seed)
    blind_inputs = {name: observation.to_dict() for name, observation in blind_observations().items()}
    for attempt in range(1, config.max_attempts + 1):
        network = _candidate(random_source)
        training_trace = _train(network, "train_enemy", TRAIN_ENEMY, 0)
        training_trace.extend(_train(network, "train_food", TRAIN_FOOD, len(training_trace)))
        outcomes, inputs = _blind_test(network)
        if _passes(outcomes):
            return SearchResult(config.seed, attempt, True, network, outcomes, inputs, training_trace)
    return SearchResult(config.seed, config.max_attempts, False, None, {}, blind_inputs, [])


def train_observations() -> tuple[Observation, Observation]:
    return TRAIN_ENEMY, TRAIN_FOOD


def blind_observations() -> dict[str, Observation]:
    return {"enemy": ENEMY, "food": FOOD, "noise": NOISE}
