from math import sqrt
import numpy as np
import scipy.sparse as sp
from modl.decomposition.recsys import RecsysDictFact, compute_biases
from modl.utils.recsys.cross_validation import train_test_split
from numpy.testing import assert_almost_equal
from numpy.testing import assert_array_almost_equal
from sklearn.utils import check_array


def test_dict_completion_normalise():
    rng = np.random.RandomState(0)
    U = rng.rand(50, 3)
    V = rng.rand(3, 20)
    X = np.dot(U, V)
    mf = RecsysDictFact(n_components=3, n_epochs=1, alpha=0.001, random_state=0, verbose=0, detrend=True)
    mf.fit(X)
    Y = np.dot(mf.code_, mf.components_)
    Y += mf.col_mean_[(np.newaxis, :)]
    Y += mf.row_mean_[(:, np.newaxis)]
    Y2 = mf.predict(X).toarray()
    assert_array_almost_equal(Y, Y2)
    rmse = np.sqrt(np.mean(((X - Y) ** 2)))
    rmse2 = mf.score(X)
    assert_almost_equal(rmse, rmse2)
