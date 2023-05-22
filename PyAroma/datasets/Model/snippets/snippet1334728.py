import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_single_model_1d_array_different_length_parameters(self):
    with pytest.raises(InputParameterError):
        t = TParModel([1, 2], [3, 4, 5])
