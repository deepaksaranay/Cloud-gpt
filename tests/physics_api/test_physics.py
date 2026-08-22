from cloud_gpt.physics_api.physics import is_physics_question


def test_recognizes_physics_terms():
    assert is_physics_question("What is Newton's second law of motion?")
    assert is_physics_question("How does quantum entanglement work?")
    assert is_physics_question("Explain the concept of gravitational force.")


def test_rejects_unrelated_questions():
    assert not is_physics_question("What is the capital of France?")
    assert not is_physics_question("How do I bake a chocolate cake?")


def test_is_case_insensitive():
    assert is_physics_question("WHAT IS ENERGY?")
