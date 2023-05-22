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


@pytest.mark.parametrize('UncertClass', uncertainty_types_to_be_tested)
def test_init_fake_with_quantity(UncertClass):
    uncert = (np.arange(10).reshape(2, 5) * u.adu)
    fake_uncert = UncertClass(uncert)
    assert_array_equal(fake_uncert.array, uncert.value)
    assert (fake_uncert.array is not uncert.value)
    assert (fake_uncert.unit is u.adu)
    fake_uncert = UncertClass(uncert, copy=False)
    assert (fake_uncert.array is not uncert.value)
    assert (fake_uncert.unit is u.adu)
    fake_uncert = UncertClass(uncert, unit=u.m)
    assert_array_equal(fake_uncert.array, uncert.value)
    assert (fake_uncert.array is not uncert.value)
    assert (fake_uncert.unit is u.m)
