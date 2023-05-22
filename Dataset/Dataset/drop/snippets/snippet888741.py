import os
from typing import Callable, Iterable
import numpy as np
import pandas as pd


def get_data_args(data_dir='data'):
    'Return objects that specify p(A), p(X|A), p(Y|X,A).'
    (all_cdfs, performance, totals) = get_FICO_data(data_dir)
    all_cdfs = all_cdfs.drop(all_cdfs.index[(- 1)])
    performance = performance.drop(performance.index[(- 1)])
    cdfs = all_cdfs[['White', 'Black']]
    cdf_B = cdfs['White'].values
    cdf_A = cdfs['Black'].values
    repay_B = performance['White']
    repay_A = performance['Black']
    scores = cdfs.index
    scores_list = scores.tolist()
    loan_repaid_probs = [_loan_repaid_probs_factory(repay_A, scores), _loan_repaid_probs_factory(repay_B, scores)]
    inv_cdfs = get_inv_cdf_fns(cdfs)
    pi_A = _get_pmf(cdf_A)
    pi_B = _get_pmf(cdf_B)
    pis = np.vstack([pi_A, pi_B])
    group_ratio = np.array((totals['Black'], totals['White']))
    group_size_ratio = (group_ratio / group_ratio.sum())
    rate_indices = (list(reversed((1 - cdf_A))), list(reversed((1 - cdf_B))))
    return (inv_cdfs, loan_repaid_probs, pis, group_size_ratio, scores_list, rate_indices)
