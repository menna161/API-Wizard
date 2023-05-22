import copy
import dataclasses
import numpy as np
import pandas as pd
from whynot.framework import GenericExperiment, parameter
from whynot.simulators import schelling
import whynot.utils as utils


@parameter(name='education_pc', default=0.3, values=np.arange(0.0, 0.99, 0.05), description='Random fraction of the population to educate')
@parameter(name='education_boost', default=(- 1), values=[(- 1), (- 2), (- 3), (- 4)], description='How much education decreases homophily')
def run_schelling(education_pc, education_boost, num_samples=100, seed=None, show_progress=False, parallelize=True):
    'Run a basic RCT experiment on Schelling.\n\n    Each unit in the experiment is a grid or "community" in the Schelling model.\n    Treatment corresponds to randomly educating some fraction of the\n    agents in the grid to decrease their homophiliy. The measure outcome is the\n    fraction of segregated agents on the grids. In this experiment, treatment is\n    randomly assigned.\n\n    Parameters\n    ----------\n        education_pc: float\n            What percentrage of the population of the treated units should be "educated"\n        education_boost: int\n            How much receiving "education" changes the homophily of an agent\n            Values in [-1, -2, -3, -4]\n        num_samples: int\n            How many units to sample for the experiment\n        seed: int\n            (Optional) Seed global randomness for the experiment\n        show_progress: bool\n            (Optional) Whether or not to print a progress bar\n        parallelize: bool\n            (Optional) Whether or not to use parallelism during the experiment\n\n    Returns\n    -------\n        covariates: np.ndarray\n            Array of shape [num_samples, num_features], observed covariates for\n            each unit.\n        treatment: np.ndarray\n            Array of shape [num_samples], treatment assignment for each unit\n        outcomes: np.ndarray\n            Array of shape [num_samples], observed outcome for each unit\n        ground_truth: np.ndarray\n            Array of shape [num_samples], unit level treatment effects\n\n    '
    rng = np.random.RandomState(seed)
    configs = []
    for _ in range(num_samples):
        config = schelling.Config()
        config.height = 10
        config.width = 10
        config.homophily = 5
        config.density = rng.uniform(0.05, 0.6)
        config.minority_pc = rng.uniform(0.05, 0.45)
        config.education_boost = education_boost
        config.education_pc = 0.0
        treatment_config = copy.deepcopy(config)
        treatment_config.education_pc = education_pc
        seed = rng.randint(0, 99999)
        configs.append((config, treatment_config, seed))
    if parallelize:
        runs = utils.parallelize(run_simulator, configs, show_progress=show_progress)
    else:
        runs = [run_simulator(*args) for args in configs]
    control_outcomes = np.array([run[0] for run in runs])
    treatment_outcomes = np.array([run[1] for run in runs])
    dataframe = pd.DataFrame([dataclasses.asdict(config[0]) for config in configs])
    covariates = dataframe[['density', 'minority_pc']].values
    treatment = (rng.rand(num_samples) < 0.25).astype(np.int32)
    treatment_idxs = np.where((treatment == 1.0))[0]
    outcomes = np.copy(control_outcomes)
    outcomes[treatment_idxs] = treatment_outcomes[treatment_idxs]
    treatment_effects = (treatment_outcomes - control_outcomes)
    return ((covariates, treatment, outcomes), treatment_effects)
