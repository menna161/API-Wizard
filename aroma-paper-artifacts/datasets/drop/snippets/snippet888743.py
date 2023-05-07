import os
from typing import Callable, Iterable
import numpy as np
import pandas as pd


def get_marginal_loan_repaid_probs(data_dir='data'):
    'Return object that specifies distn p(Y|X).'
    (all_cdfs, performance, totals) = get_FICO_data(data_dir)
    all_cdfs = all_cdfs.drop(all_cdfs.index[(- 1)])
    performance = performance.drop(performance.index[(- 1)])
    cdfs = all_cdfs[['White', 'Black']]
    repay_B = performance['White']
    repay_A = performance['Black']
    scores = cdfs.index
    group_ratio = np.array((totals['Black'], totals['White']))
    group_size_ratio = (group_ratio / group_ratio.sum())
    (p_A, p_B) = group_size_ratio
    repay_marginal = ((repay_A * p_A) + (repay_B * p_B))
    loan_repaid_probs = _loan_repaid_probs_factory(repay_marginal, scores)
    loan_repaid_probs = [loan_repaid_probs, loan_repaid_probs]
    return loan_repaid_probs
