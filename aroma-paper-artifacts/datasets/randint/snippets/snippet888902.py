import dataclasses
from mesa.batchrunner import BatchRunner
import numpy as np
from whynot.simulators.schelling.model import Schelling


def simulate(config, rollouts=10, seed=None):
    'Simulate repeated runs of the Schelling model for config.\n\n    Parameters\n    ----------\n        config: whynot.simulators.Schelling\n            Configuration of the grid, agent properties, and model dynamics.\n        rollouts: int\n            How many times to run the model for the same configuration.\n        seed: int\n            (Optional) Seed all randomness in rollouts\n\n    Returns\n    -------\n        segregated_fraction: pd.Series\n            What fraction of the agents are segrated at the end of the run\n            for each rollout.\n\n    '
    model_reporters = {'Segregated_Agents': get_segregation}
    rng = np.random.RandomState(seed)
    param_sweep = BatchRunner(Schelling, fixed_parameters=dataclasses.asdict(config), max_steps=200, model_reporters=model_reporters, display_progress=False, variable_parameters={'seed': rng.randint(9999999, size=rollouts)}, iterations=1)
    param_sweep.run_all()
    dataframe = param_sweep.get_model_vars_dataframe()
    return dataframe.Segregated_Agents.mean()
