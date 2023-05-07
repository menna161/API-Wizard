import copy
import dataclasses
from scipy.integrate import odeint
import whynot as wn
import whynot.traceable_numpy as np
from whynot.dynamics import BaseConfig, BaseIntervention, BaseState


def simulate(initial_state, config, intervention=None, seed=None):
    'Simulate a run of the Chen et al. model opioid epidemic model.\n\n    Parameters\n    ----------\n        initial_state: whynot.simulator.opioid.State\n            Initial state of the dynamics\n        config: whynot.simulator.opioid.Config\n            Config object to determine simulation dynamics.\n        intervention: whynot.simulator.opioid.Intervention\n            (Optional) Intervention object to determine what, if any,\n            intervention to perform during the rollout of the dynamics.\n        seed: int\n            The simulator is deterministic, so the seed parameter is ignored.\n\n    Returns\n    -------\n        run: whynot.dynamics.Run\n            Run object produced by running simulate for the opioid simulator\n\n    '
    t_eval = np.arange(config.start_time, (config.end_time + config.delta_t), config.delta_t)
    solution = odeint(dynamics, y0=dataclasses.astuple(initial_state), t=t_eval, args=(config, intervention), rtol=0.0001, atol=0.0001)
    states = ([initial_state] + [State(*state) for state in solution[1:]])
    return wn.dynamics.Run(states=states, times=t_eval)
