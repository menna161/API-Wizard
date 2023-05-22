import os
import numpy as np
import pandas as pd
from whynot.framework import GenericExperiment, parameter


@parameter(name='hidden_dim', default=32, values=[8, 16, 32, 64, 128, 256, 512], description='hidden dimension of 2-layer ReLu network response.')
@parameter(name='alpha_scale', default=0.01, values=np.linspace(0.0001, 10, 10), description='Scale of the hidden-layer weights.')
def run_lalonde(num_samples, hidden_dim, alpha_scale, seed=None, parallelize=True, show_progress=False):
    'Generate data from the LaLonde dataset with a random response function.\n\n    The covariates and treatment are both specified by the dataset, and the\n    response function is a random 2-layer neural network with ReLu.\n\n    Parameters\n    ----------\n        num_samples: int\n            This parameter is ignored since the LaLonde dataset size is fixed.\n        hidden_dim: int\n            Hidden dimension of the relu network.\n        alpha_scale: float\n            Standard deviation of the final layer weights.\n        seed: int\n            Random seed used for all internal randomness\n        parallelize: bool\n            Ignored, but included for consistency with GenericExperiment API.\n        show_progress: False\n            Ignored, but included for consistency with GenericExperiment API.\n\n    '
    rng = np.random.RandomState(seed)
    dataset = load_dataset()
    treatment = dataset.treatment.values.astype(np.int64)
    covariates = dataset.drop('treatment', axis=1).values
    num_inputs = covariates.shape[1]
    control_config = {'W': (0.05 * rng.randn(num_inputs, hidden_dim)), 'alpha': (alpha_scale * rng.randn(hidden_dim, 1))}
    treatment_config = {'W': (0.05 * rng.randn(num_inputs, hidden_dim)), 'alpha': (alpha_scale * rng.randn(hidden_dim, 1))}

    def get_effect(features, treatment):
        if treatment:
            config = treatment_config
        else:
            config = control_config
        return np.maximum(features.dot(config['W']), 0).dot(config['alpha'])[(:, 0)]
    control_outcomes = get_effect(covariates, treatment=False)
    treatment_outcomes = get_effect(covariates, treatment=True)
    outcomes = np.copy(control_outcomes)
    treatment_idxs = np.where((treatment == 1.0))
    outcomes[treatment_idxs] = treatment_outcomes[treatment_idxs]
    return ((covariates, treatment, outcomes), (treatment_outcomes - control_outcomes))
