import numpy as np
from whynot.dynamics import DynamicsExperiment
from whynot.framework import parameter
from whynot.simulators import lotka_volterra


@parameter(name='propensity', default=0.9, values=np.linspace(0.5, 0.99, 10), description='Probability of treatment for group with low fox population.')
def confounded_propensity_scores(untreated_run, propensity=0.9):
    "Return confounded treatment assignment probability.\n\n    Treatment increases fox population growth. Therefore, we're assume\n    treatment is more likely for runs with low initial fox population.\n    "
    if (untreated_run.initial_state.foxes < 20):
        return propensity
    return (1.0 - propensity)
