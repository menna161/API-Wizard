import numpy as np
import cma


def compute_ranks(x):
    '\n  Returns ranks in [0, len(x))\n  Note: This is different from scipy.stats.rankdata, which returns ranks in [1, len(x)].\n  (https://github.com/openai/evolution-strategies-starter/blob/master/es_distributed/es.py)\n  '
    assert (x.ndim == 1)
    ranks = np.empty(len(x), dtype=int)
    ranks[x.argsort()] = np.arange(len(x))
    return ranks
