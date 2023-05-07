import copy
import dataclasses
import inspect
import numpy as np
from tqdm.auto import tqdm
from whynot.framework import Dataset, extract_params, ParameterCollection
from whynot import causal_graphs, utils


def _run_all_simulations(self, initial_states, config, intervention, rng, parallelize, show_progress):
    'Run simulation for treated and untreated groups for each initial state.\n\n        Parameters\n        ----------\n            initial_state: list\n                List of initial state objects\n            config: `Config`\n                Configuration object for all runs of the simulator.\n            intervention: `Intervention`\n                Intervention object for treated runs of the simulator.\n            rng: `np.random.RandomState`\n                Source of randomness. Used to choose seeds for different simulator runs.\n            parallelize: bool\n                Whether or not to execute runs of the simulator in parallel or sequentially.\n            show_progress: bool\n                Whether or not to display a progress bar for simulator execution.\n\n        Returns\n        -------\n            untreated_runs: `list[Run]`\n                List of simulator runs in untreated group, one for each initial state.\n            treated_runs: `list[Run]`\n                List of simulator runs in treated group, one for each initial state.\n\n        '
    parallel_args = []
    for state in initial_states:
        seed = rng.randint(0, ((2 ** 32) - 1))
        parallel_args.append((self.simulator.simulate, config, intervention, state, seed))
    if parallelize:
        runs = utils.parallelize(self._run_dynamics_simulator, parallel_args, show_progress=show_progress)
    elif show_progress:
        runs = [self._run_dynamics_simulator(*args) for args in tqdm(parallel_args)]
    else:
        runs = [self._run_dynamics_simulator(*args) for args in parallel_args]
    (untreated_runs, treated_runs) = list(zip(*runs))
    return (untreated_runs, treated_runs)
