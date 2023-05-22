import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.modeling.core import Model
from astropy.modeling.models import Gaussian1D, Shift, Scale, Pix2Sky_TAN
from astropy import units as u
from astropy.units import UnitsError
from astropy.tests.helper import assert_quantity_allclose


def setup_method(self, method):
    self.model = MyTestModel()
