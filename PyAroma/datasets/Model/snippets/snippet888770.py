from contextlib import contextmanager
import copy
import dataclasses
import os
import sys
import numpy as np
import pyomo
from pyomo.environ import RangeSet, ConcreteModel, NonNegativeReals, Reals, Var, Constraint, Objective, summation, log, maximize
import whynot as wn
from whynot.dynamics import BaseConfig, BaseIntervention, BaseState


def simulate(initial_state, config, intervention=None, seed=None, stochastic=True):
    'Simulate a run of the DICE model.\n\n    Parameters\n    ----------\n        initial_state: whynot.simulators.dice.State\n            Initial state of for a run of the DICE model\n        config: whynot.simulators.dice.Config\n            Configuration object to set parameters of the dynamics.\n        intervention:  whynot.simulators.dice.Intervention\n            (Optional) What, if any, intervention to perform during execution.\n        seed: int\n            (Optional) Random seed for all model randomness.\n        stochastic: bool\n            (Optional) Whether or not to apply a random perturbation to the dynamics.\n\n    Returns\n    -------\n        run: whynot.dynamics.Run\n            Sequence of states and corresponding timesteps generated during execution.\n\n    '
    if intervention:
        config = config.update(intervention)
    rng = np.random.RandomState(seed)
    model = ConcreteModel()
    model.time = RangeSet(1, config.numPeriods, 1)
    if stochastic:
        config = copy.deepcopy(config)
        config.t2xco2 *= rng.uniform(low=0.9, high=1.1)
        config.fosslim *= rng.uniform(low=0.9, high=1.1)
        config.limmiu *= rng.uniform(low=0.9, high=1.1)
        config.dsig *= rng.uniform(low=0.9, high=1.1)
        config.pop0 *= rng.uniform(low=0.9, high=1.1)
    initialize_model(model, initial_state, config)
    add_emissions_dynamics(model, config)
    add_climate_dynamics(model, config)
    add_economic_dynamics(model, config)
    model.UTILITY = Var(domain=Reals)
    add_utility_dynamics(model, config)
    model.OBJ = Objective(rule=(lambda m: m.UTILITY), sense=maximize)
    solver = get_ipopt_solver()
    with silence_stdout():
        _ = solver.solve(model, tee=True, symbolic_solver_labels=True, keepfiles=False, options={'max_iter': 99900, 'halt_on_ampl_error': 'yes', 'print_level': 0})
    (states, times) = ([initial_state], [0])
    for time in range(1, (config.numPeriods + 1)):
        state = State()
        for var in state.variables:
            state[var] = getattr(model, var)[time].value
        states.append(state)
        times.append(time)
    return wn.dynamics.Run(states=states, times=times)
