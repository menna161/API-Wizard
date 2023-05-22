import numpy as np
from whynot.dynamics import DynamicsExperiment
from whynot.framework import parameter
from whynot.simulators import lotka_volterra


@parameter(name='propensity', default=0.1, values=np.linspace(0.05, 0.5, 10), description='Probability of treatment')
def rct_propensity(propensity):
    'Return constant propensity for RCT.'
    return propensity
