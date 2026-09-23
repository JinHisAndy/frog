from frog.model import Frame, Observation
from frog.network import Network
from frog.search import SearchResult, blind_observations


def build_replay(result: SearchResult) -> list[Frame]:
    if not result.found or result.network is None:
        return []

    frames = list(result.training_trace)
    index = len(frames)
    for name, observation in blind_observations().items():
        frames.extend(_blind_scenario_frames(result.network, f"blind_{name}", observation, index))
        index = len(frames)
    return frames


def _blind_scenario_frames(
    network: Network,
    label: str,
    observation: Observation,
    start_index: int,
) -> list[Frame]:
    simulated = network.clone()
    frames: list[Frame] = []
    simulated.reset()
    simulated.set_observation(observation)
    frames.append(
        Frame(
            index=start_index,
            phase=label,
            message=f"{label}: blind-test external signals entered the receptor layer",
            observation=observation,
            network=simulated.to_dict(),
        )
    )
    simulated.evaluate_layer(0)
    frames.append(
        Frame(
            index=start_index + 1,
            phase=label,
            message=f"{label}: blind-test input threshold evaluation completed",
            observation=observation,
            active_chemicals=sorted(simulated.active_chemicals(), key=str),
            network=simulated.to_dict(),
        )
    )
    highest_layer = max(node.layer for node in simulated.nodes.values())
    for source_layer in range(highest_layer):
        simulated.propagate_from_layer(source_layer)
        simulated.evaluate_layer(source_layer + 1)
        frames.append(
            Frame(
                index=start_index + len(frames),
                phase=label,
                message=f"{label}: blind-test propagated from layer {source_layer}",
                observation=observation,
                active_chemicals=sorted(simulated.active_chemicals(), key=str),
                network=simulated.to_dict(),
            )
        )
    action = simulated.forward(observation, learn=False)
    frames.append(
        Frame(
            index=start_index + len(frames),
            phase=label,
            message=f"{label}: blind-test action settled; learning=disabled",
            observation=observation,
            active_chemicals=sorted(simulated.active_chemicals(), key=str),
            action=action,
            network=simulated.to_dict(),
        )
    )
    return frames
