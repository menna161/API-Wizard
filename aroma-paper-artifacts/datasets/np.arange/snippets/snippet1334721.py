import itertools
import pytest
import numpy as np
from . import irafutil
from astropy.modeling import models, fitting
from astropy.modeling.core import Model, FittableModel
from astropy.modeling.parameters import Parameter, InputParameterError
from astropy.utils.data import get_pkg_data_filename


def setup_class(self):
    self.x1 = np.arange(1, 10, 0.1)
    (self.y, self.x) = np.mgrid[(:10, :7)]
    self.x11 = np.array([self.x1, self.x1]).T
    self.gmodel = models.Gaussian1D([12, 10], [3.5, 5.2], stddev=[0.4, 0.7], n_models=2)
