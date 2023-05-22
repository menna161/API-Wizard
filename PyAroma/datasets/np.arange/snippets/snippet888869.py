import dataclasses
import numpy as np
from scipy.integrate import odeint
import whynot as wn
from whynot.dynamics import BaseConfig, BaseIntervention, BaseState


def simulate(initial_state, config, intervention=None, seed=None):
    'Simulate a run of the Lotka volterra model.\n\n    Parameters\n    ----------\n        initial_state: whynot.lotka_volterra.State\n        config: whynot.lotka_volterra.Config\n            Base parameters for the simulator run\n        intervention: whynot.lotka_volterra.Intervention\n            (Optional) Parameters specifying a change in dynamics\n        seed: int\n            Unused since the simulator is deterministic.\n\n    Returns\n    -------\n        run: whynot.dynamics.Run\n            Simulator rollout\n\n    '
    t_eval = np.arange(config.start_time, (config.end_time + config.delta_t), config.delta_t)
    solution = odeint(dynamics, y0=dataclasses.astuple(initial_state), t=t_eval, args=(config, intervention), rtol=0.0001, atol=0.0001)
    states = ([initial_state] + [State(*state) for state in solution[1:]])
    return wn.dynamics.Run(states=states, times=t_eval)
