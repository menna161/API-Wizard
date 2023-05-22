import numpy as np
from whynot.dynamics import DynamicsExperiment
from whynot.framework import parameter
from whynot.simulators import world3


@parameter(name='treatment_bias', default=0.8, values=np.linspace(0.5, 1.0, 5), description='Treatment probability bias between low and high pollution runs.')
def pollution_confounded_propensity(intervention, untreated_runs, treatment_bias):
    'Probability of treating each unit.\n\n    To generate confounding, we are more likely to treat worlds with high pollution.\n    '

    def persistent_pollution(run):
        return run[intervention.time].persistent_pollution
    pollution = [persistent_pollution(run) for run in untreated_runs]
    upper_quantile = np.quantile(pollution, 0.9)

    def treatment_prob(idx):
        if (pollution[idx] > upper_quantile):
            return treatment_bias
        return (1.0 - treatment_bias)
    return np.array([treatment_prob(idx) for idx in range(len(untreated_runs))])
