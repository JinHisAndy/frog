from frog.experiments.stage06_one_pixel_reflex.engine import train_one_pixel_reflex


def test_one_pixel_reflex_predicts_feedback_when_feedback_is_hidden():
    model = train_one_pixel_reflex(training=[(True, True), (False, False)])

    assert model.act(True).bite is True
    assert model.act(False).bite is False


def test_untrained_reflex_does_not_claim_prediction():
    model = train_one_pixel_reflex(training=[])

    assert model.act(True).bite is False
