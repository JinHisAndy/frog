from frog.experiments.stage07_two_pixel_reflex.engine import evaluate, train_two_pixel_reflex


def test_two_pixel_model_learns_xor_like_mapping_then_predicts_without_feedback():
    model = train_two_pixel_reflex(
        training=[
            ((False, False), False),
            ((False, True), True),
            ((True, False), True),
            ((True, True), False),
        ]
    )

    report = evaluate(model, [((False, True), True), ((True, True), False)])

    assert report.accuracy == 1.0
    assert model.act((False, True)).bite is True
    assert model.act((True, True)).bite is False


def test_two_pixel_evaluation_reports_confusion_matrix():
    model = train_two_pixel_reflex(training=[((True, False), True)])

    report = evaluate(model, [((True, False), True), ((False, False), False)])

    assert report.total == 2
    assert report.true_positive == 1
