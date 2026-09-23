from frog.life.learning import ReflexMemory


def test_reflex_memory_turns_delayed_reward_into_future_prediction():
    memory = ReflexMemory()

    memory.observe(pattern=(True, False), action="bite", outcome=1)
    memory.observe(pattern=(False, True), action="bite", outcome=-1)

    assert memory.predict((True, False)) == "bite"
    assert memory.predict((False, True)) == "avoid"


def test_reflex_memory_returns_explore_when_pattern_has_no_evidence():
    assert ReflexMemory().predict((True, True)) == "explore"
