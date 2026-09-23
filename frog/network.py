from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .model import Action, Chemical, Link, Node, Observation


INPUT_NAMES = ("pixel_a", "pixel_b", "pixel_c", "pixel_d", "pain", "sweet")
FLEE = "flee"
BITE = "bite"


@dataclass
class Network:
    nodes: dict[str, Node]
    links: list[Link] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.nodes:
            raise ValueError("network must contain at least one node")
        for identifier, node in self.nodes.items():
            if identifier != node.identifier:
                raise ValueError(f"node key {identifier!r} does not match node id {node.identifier!r}")
            if node.layer < 0:
                raise ValueError(f"node {identifier!r} has a negative layer")
        for link in self.links:
            if link.source not in self.nodes or link.target not in self.nodes:
                raise ValueError(f"link {link.source!r}->{link.target!r} references an unknown node")
            if self.nodes[link.source].layer >= self.nodes[link.target].layer:
                raise ValueError(
                    f"link {link.source!r}->{link.target!r} must point forward to a higher layer"
                )

    def clone(self) -> "Network":
        return Network.from_dict(self.to_dict())

    def reset(self) -> None:
        for node in self.nodes.values():
            node.reset()

    def set_observation(self, observation: Observation) -> None:
        values = (*observation.pixels, observation.pain, observation.sweet)
        for name, value in zip(INPUT_NAMES, values, strict=True):
            self.nodes[name].current_input = 100.0 if value else 0.0

    def evaluate_layer(self, layer: int) -> None:
        for node in self.nodes.values():
            if node.layer == layer:
                node.evaluate()

    def propagate_from_layer(self, source_layer: int) -> None:
        for link in self.links:
            source = self.nodes[link.source]
            if source.layer == source_layer and source.activated:
                self.nodes[link.target].current_input += link.weight

    def active_chemicals(self) -> set[Chemical]:
        return {
            node.chemical
            for node in self.nodes.values()
            if node.activated and node.chemical is not Chemical.NONE
        }

    def apply_plasticity(self, active_chemicals: Iterable[Chemical]) -> None:
        active = set(active_chemicals)
        for link in self.links:
            if link.modulated_by in active:
                link.weight = max(0.0, min(100.0, link.weight + link.plasticity_delta))

    def forward(self, observation: Observation, *, learn: bool) -> Action:
        self.reset()
        self.set_observation(observation)
        self.evaluate_layer(0)
        highest_layer = max(node.layer for node in self.nodes.values())
        for source_layer in range(highest_layer):
            self.propagate_from_layer(source_layer)
            self.evaluate_layer(source_layer + 1)
        action = Action(flee=self.nodes[FLEE].activated, bite=self.nodes[BITE].activated)
        if learn:
            self.apply_plasticity(self.active_chemicals())
        return action

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "links": [link.to_dict() for link in self.links],
        }

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> "Network":
        node_values = value["nodes"]
        link_values = value["links"]
        if not isinstance(node_values, list) or not isinstance(link_values, list):
            raise ValueError("network data must contain node and link lists")
        nodes = {
            str(node_value["id"]): Node(
                identifier=str(node_value["id"]),
                threshold=float(node_value["threshold"]),
                chemical=Chemical(str(node_value["chemical"])),
                layer=int(node_value["layer"]),
                current_input=float(node_value.get("current_input", 0.0)),
                activated=bool(node_value.get("activated", False)),
            )
            for node_value in node_values
            if isinstance(node_value, dict)
        }
        links = [
            Link(
                source=str(link_value["source"]),
                target=str(link_value["target"]),
                weight=float(link_value["weight"]),
                modulated_by=Chemical(str(link_value["modulated_by"])),
                plasticity_delta=float(link_value["plasticity_delta"]),
            )
            for link_value in link_values
            if isinstance(link_value, dict)
        ]
        return cls(nodes=nodes, links=links)
