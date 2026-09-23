from frog.model import Chemical, Frame, Observation
from frog.network import Network
from frog.search import SearchResult, blind_observations, train_observations


def build_replay(result: SearchResult) -> list[Frame]:
    if not result.found or result.network is None:
        return []

    frames: list[Frame] = []
    index = 0
    for label, observation, learn in (
        ("train_enemy", train_observations()[0], True),
        ("train_food", train_observations()[1], True),
        *[(f"blind_{name}", observation, False) for name, observation in blind_observations().items()],
    ):
        frames.extend(_scenario_frames(result.network, label, observation, learn, index))
        index = len(frames)
    return frames


def _scenario_frames(network: Network, label: str, observation: Observation, learn: bool, start_index: int) -> list[Frame]:
    simulated = network.clone()
    frames: list[Frame] = []
    simulated.reset()
    simulated.set_observation(observation)
    frames.append(
        Frame(
            index=start_index,
            phase=label,
            message=f"{label}: external signals entered the receptor layer",
            observation=observation,
            network=simulated.to_dict(),
        )
    )
    simulated.evaluate_layer(0)
    frames.append(
        Frame(
            index=start_index + 1,
            phase=label,
            message=f"{label}: input threshold evaluation completed",
            observation=observation,
            active_chemicals=sorted(simulated.active_chemicals(), key=str),
            network=simulated.to_dict(),
        )
    )
    for layer in (1, 2):
        simulated.propagate()
        simulated.evaluate_layer(layer)
        active = sorted(simulated.active_chemicals(), key=str)
        frames.append(
            Frame(
                index=start_index + len(frames),
                phase=label,
                message=f"{label}: propagated to layer {layer}",
                observation=observation,
                active_chemicals=active,
                network=simulated.to_dict(),
            )
        )
    action = simulated.forward(observation, learn=learn)
    frames.append(
        Frame(
            index=start_index + len(frames),
            phase=label,
            message=f"{label}: action settled; learning={'enabled' if learn else 'disabled'}",
            observation=observation,
            active_chemicals=sorted(simulated.active_chemicals(), key=str),
            action=action,
            network=simulated.to_dict(),
        )
    )
    return frames
