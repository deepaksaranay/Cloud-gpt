"""Heuristic check for whether a question is about physics."""

PHYSICS_KEYWORDS = {
    "physics", "force", "energy", "mass", "velocity", "acceleration", "momentum",
    "gravity", "gravitational", "quantum", "relativity", "thermodynamics", "entropy",
    "electric", "electricity", "magnetic", "magnetism", "electromagnetic", "wave",
    "frequency", "wavelength", "particle", "atom", "atomic", "nuclear", "photon",
    "electron", "proton", "neutron", "friction", "pressure", "pendulum", "motion",
    "kinetic", "potential", "torque", "optics", "refraction", "light", "sound", "heat",
    "temperature", "field", "charge", "current", "voltage", "resistance", "circuit",
    "newton", "einstein", "mechanics", "dynamics", "kinematics", "spacetime",
    "black hole", "orbit", "inertia",
}


def is_physics_question(question: str) -> bool:
    """Return True if the question contains at least one recognizable physics term."""
    lowered = question.lower()
    return any(keyword in lowered for keyword in PHYSICS_KEYWORDS)
