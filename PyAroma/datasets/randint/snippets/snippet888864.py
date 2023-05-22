import numpy as np
from whynot.dynamics import DynamicsExperiment
from whynot.framework import parameter
from whynot.simulators import lotka_volterra


def sample_initial_states(rng):
    'Sample an initial state for the LV model.'
    rabbits = rng.randint(10, 100)
    foxes = (rng.uniform(0.1, 0.8) * rabbits)
    return lotka_volterra.State(rabbits=rabbits, foxes=foxes)
