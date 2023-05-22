import dataclasses
import numpy as np
from scipy.integrate import odeint
import whynot as wn
from whynot.dynamics import BaseConfig, BaseState, BaseIntervention
from whynot.simulators.world2 import tables


def simulate(initial_state, config, intervention=None, seed=None):
    'Run a simulation of the world2 dynamics from the given initial state.\n\n    Parameters\n    ----------\n        initial_state: whynot.simulators.world2.State\n            State object to initialize the simulation\n        config: whynot.simulators.world2.Config\n            Configuration object to determine coefficients of the dynamics.\n        intervention: whynot.simulators.world2.Intervention\n            (Optional) Specify what, if any, intervention to perform during execution.\n        seed: int\n            (Optional) The simulator is deterministic, and the seed parameter is ignored.\n\n    Returns\n    -------\n        run: whynot.dynamics.Run\n            Rollout sequence of states and measurement times produced by the simulator.\n\n    '
    t_eval = np.arange(config.start_time, (config.end_time + config.delta_t), config.delta_t)
    solution = odeint(dynamics, y0=dataclasses.astuple(initial_state), t=t_eval, args=(config, intervention), rtol=config.rtol, atol=config.atol)
    states = ([initial_state] + [State(*state) for state in solution[1:]])
    return wn.dynamics.Run(states=states, times=t_eval)
