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


@pytest.mark.parametrize('t, min_leaf', zip(tt, min_leafs))
def test__compute_valid_splitting_indices_with_empty_output(t, min_leaf):
    out = _compute_valid_splitting_indices(t, min_leaf)
    assert_array_equal(out, np.arange(0))
