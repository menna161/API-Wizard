import types
import pytest
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import RandomState
from astropy.modeling.core import Fittable1DModel
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyUserWarning
from .utils import ignore_non_integer_warning
from scipy import optimize
from astropy.utils import NumpyRNGContext


def setup_class(self):
    A = (- 2.0)
    B = 0.5
    self.x = np.linspace((- 1.0), 1.0, 100)
    self.y = (((A * self.x) + B) + np.random.normal(scale=0.1, size=100))
    data = np.array([505.0, 556.0, 630.0, 595.0, 561.0, 553.0, 543.0, 496.0, 460.0, 469.0, 426.0, 518.0, 684.0, 798.0, 830.0, 794.0, 649.0, 706.0, 671.0, 545.0, 479.0, 454.0, 505.0, 700.0, 1058.0, 1231.0, 1325.0, 997.0, 1036.0, 884.0, 610.0, 487.0, 453.0, 527.0, 780.0, 1094.0, 1983.0, 1993.0, 1809.0, 1525.0, 1056.0, 895.0, 604.0, 466.0, 510.0, 678.0, 1130.0, 1986.0, 2670.0, 2535.0, 1878.0, 1450.0, 1200.0, 663.0, 511.0, 474.0, 569.0, 848.0, 1670.0, 2611.0, 3129.0, 2507.0, 1782.0, 1211.0, 723.0, 541.0, 511.0, 518.0, 597.0, 1137.0, 1993.0, 2925.0, 2438.0, 1910.0, 1230.0, 738.0, 506.0, 461.0, 486.0, 597.0, 733.0, 1262.0, 1896.0, 2342.0, 1792.0, 1180.0, 667.0, 482.0, 454.0, 482.0, 504.0, 566.0, 789.0, 1194.0, 1545.0, 1361.0, 933.0, 562.0, 418.0, 463.0, 435.0, 466.0, 528.0, 487.0, 664.0, 799.0, 746.0, 550.0, 478.0, 535.0, 443.0, 416.0, 439.0, 472.0, 472.0, 492.0, 523.0, 569.0, 487.0, 441.0, 428.0])
    self.data = data.reshape(11, 11)
