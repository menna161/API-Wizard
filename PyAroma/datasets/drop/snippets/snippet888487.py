import os
import numpy as np
import pandas as pd
import whynot as wn


def test_gams():
    'Ensure calling default simulator has results reflective of the GAMS implementaiton'
    gams_file = (os.path.realpath(__file__).rsplit('/', 1)[0] + '/gamsBaseline.csv')
    gams = pd.read_csv(gams_file).replace([np.inf, (- np.inf)], np.nan).fillna(0)
    gams.columns = ['Variable', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    gams.drop('Variable', axis=1, inplace=True)
    config = wn.dice.Config(numPeriods=10, ifopt=0)
    initial_state = wn.dice.State()
    run = wn.dice.simulate(initial_state, config, stochastic=False)
    sim_dict = {var: [getattr(state, var) for state in run.states[1:]] for var in initial_state.variables}
    sim = pd.DataFrame.from_dict(sim_dict, orient='index', columns=gams.columns).replace([np.inf, (- np.inf)], np.nan).fillna(0)
    np.testing.assert_allclose(sim, gams, rtol=0.0001, atol=0.05, equal_nan=False)
