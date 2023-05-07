import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_array_parameter1(self):
    with pytest.raises(InputParameterError):
        t = TParModel(np.array([[1, 2], [3, 4]]), 1, model_set_axis=0)
