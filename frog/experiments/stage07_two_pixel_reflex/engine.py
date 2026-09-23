from __future__ import annotations

from .model import EvaluationReport, TwoPixelReflex


def train_two_pixel_reflex(*, training: list[tuple[tuple[bool, bool], bool]]) -> TwoPixelReflex:
    grouped: dict[tuple[bool, bool], list[bool]] = {}
    for pixels, sweet_feedback in training:
        grouped.setdefault(pixels, []).append(sweet_feedback)
    return TwoPixelReflex(
        table={pixels: sum(labels) * 2 >= len(labels) for pixels, labels in grouped.items()}
    )


def evaluate(model: TwoPixelReflex, cases: list[tuple[tuple[bool, bool], bool]]) -> EvaluationReport:
    tp = tn = fp = fn = 0
    for pixels, expected_bite in cases:
        actual_bite = model.act(pixels).bite
        if actual_bite and expected_bite:
            tp += 1
        elif not actual_bite and not expected_bite:
            tn += 1
        elif actual_bite:
            fp += 1
        else:
            fn += 1
    return EvaluationReport(tp, tn, fp, fn)
