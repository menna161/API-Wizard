import numpy as np
import unittest
import logging
from FMin import fmin, load_func, load_configspace
import ConfigSpace as CS
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

if (__name__ == '__main__'):
    unittest.main()
    cs = CS.ConfigurationSpace()
    cs.add_hyperparameter(CS.UniformFloatHyperparameter('w', lower=(- 5), upper=5))
    X = np.random.uniform((- 5), 5, 100)
    y = np.random.normal(X, 1)
    opt_func = (lambda x, y, w, budget: np.mean(((y[:int(budget)] - (w * x[:int(budget)])) ** 2)))
    for w in cs.sample_configuration(size=3):
        print('W: {} --> {}'.format(w['w'], opt_func(X, y, **w, budget=3)))
    (inc_value, inc_cfg, result) = fmin(opt_func, cs, func_args=(X, y), min_budget=3, max_budget=len(X), num_iterations=3, num_workers=1)
    id2config = result.get_id2config_mapping()
    incumbent = result.get_incumbent_id()
    traj = result.get_incumbent_trajectory()
    budgets = [b for b in traj['budgets']]
    values = [id2config[id]['config'] for id in traj['config_ids']]
    import matplotlib.pyplot as plt
    plt.scatter(X, y)
    plt.xlim((- 5), 5)
    plt.ylim((- 5), 5)
    for i in range(len(values)):
        plt.plot(X, (values[i]['w'] * X), label='{}. W: {:.2f}'.format((i + 1), values[i]['w']))
    plt.legend(loc=1)
    plt.show()
