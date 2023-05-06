import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal
from cforest.tree import _compute_global_loss
from cforest.tree import _compute_valid_splitting_indices
from cforest.tree import _find_optimal_split
from cforest.tree import _find_optimal_split_inner_loop
from cforest.tree import _predict_row_causaltree
from cforest.tree import _retrieve_index
from cforest.tree import _transform_outcome
from cforest.tree import predict_causaltree


def _create_data_for_splitting_tests(n):
    x = np.linspace((- 1), 1, num=n)
    np.random.seed(2)
    t = np.array(np.random.binomial(1, 0.5, n), dtype=bool)
    y = np.repeat([(- 1), 1], int((n / 2)))
    y = np.insert(y, int((n / 2)), (- 1))
    y = (y + ((2 * y) * t))
    return (x, t, y)
