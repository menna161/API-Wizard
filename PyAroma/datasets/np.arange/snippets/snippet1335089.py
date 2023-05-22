import pickle
import pytest
import numpy as np
from numpy.testing import assert_array_equal
from astropy.nddata.nduncertainty import StdDevUncertainty, VarianceUncertainty, InverseVariance, NDUncertainty, IncompatibleUncertaintiesException, MissingDataAssociationException, UnknownUncertainty
from astropy.nddata.nddata import NDData
from astropy.nddata.compat import NDDataArray
from astropy.nddata.ccddata import CCDData
from astropy import units as u
from collections import defaultdict
from gc import get_objects
from astropy.nddata.compat import NDDataArray


def test_init_fake_with_StdDevUncertainty():
    uncert = np.arange(5).reshape(5, 1)
    std_uncert = StdDevUncertainty(uncert)
    with pytest.raises(IncompatibleUncertaintiesException):
        FakeUncertainty(std_uncert)
    fake_uncert = FakeUncertainty(uncert)
    with pytest.raises(IncompatibleUncertaintiesException):
        StdDevUncertainty(fake_uncert)
