import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def test_wrong_number_of_params2(self):
    with pytest.raises(InputParameterError):
        m = TParModel(coeff=[[1, 2], [3, 4]], e=4, n_models=2)
    with pytest.raises(InputParameterError):
        m = TParModel(coeff=[[1, 2], [3, 4]], e=4, model_set_axis=0)
