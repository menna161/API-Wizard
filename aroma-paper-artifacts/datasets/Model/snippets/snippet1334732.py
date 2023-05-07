import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


@pytest.mark.parametrize(('p1', 'p2'), [(1, 2), (1, [2, 3]), ([1, 2], 3), ([1, 2, 3], [4, 5]), ([1, 2], [3, 4, 5])])
def test_two_model_incorrect_scalar_parameters(self, p1, p2):
    with pytest.raises(InputParameterError):
        TParModel(p1, p2, n_models=2)
