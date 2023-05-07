import dataclasses
import numpy as np
from scipy.integrate import odeint
import whynot as wn
from whynot.dynamics import BaseConfig, BaseState, BaseIntervention


def simulate(initial_state, config, intervention=None, seed=None):
    'Simulate a run of the Adams HIV simulator model.\n\n    The simulation starts at initial_state at time 0, and evolves the state\n    using dynamics whose parameters are specified in config.\n\n    Parameters\n    ----------\n        initial_state:  `whynot.simulators.hiv.State`\n            Initial State object, which is used as x_{t_0} for the simulator.\n        config:  `whynot.simulators.hiv.Config`\n            Config object that encapsulates the parameters that define the dynamics.\n        intervention: `whynot.simulators.hiv.Intervention`\n            Intervention object that specifies what, if any, intervention to perform.\n        seed: int\n            Seed to set internal randomness. The simulator is deterministic, so\n            the seed parameter is ignored.\n\n    Returns\n    -------\n        run: `whynot.dynamics.Run`\n            Rollout of the model.\n\n    '
    t_eval = np.arange(config.start_time, (config.end_time + config.delta_t), config.delta_t)
    solution = odeint(dynamics, y0=dataclasses.astuple(initial_state), t=t_eval, args=(config, intervention), rtol=config.rtol, atol=config.atol)
    states = ([initial_state] + [State(*state) for state in solution[1:]])
    return wn.dynamics.Run(states=states, times=t_eval)
