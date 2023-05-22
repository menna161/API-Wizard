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
def test_init_fake_with_fake(UncertClass):
    uncert = np.arange(5).reshape(5, 1)
    fake_uncert1 = UncertClass(uncert)
    fake_uncert2 = UncertClass(fake_uncert1)
    assert_array_equal(fake_uncert2.array, uncert)
    assert (fake_uncert2.array is not uncert)
    fake_uncert1 = UncertClass(uncert, copy=False)
    fake_uncert2 = UncertClass(fake_uncert1, copy=False)
    assert_array_equal(fake_uncert2.array, fake_uncert1.array)
    assert (fake_uncert2.array is fake_uncert1.array)
    uncert = (np.arange(5).reshape(5, 1) * u.adu)
    fake_uncert1 = UncertClass(uncert)
    fake_uncert2 = UncertClass(fake_uncert1)
    assert_array_equal(fake_uncert2.array, uncert.value)
    assert (fake_uncert2.array is not uncert.value)
    assert (fake_uncert2.unit is u.adu)
    fake_uncert2 = UncertClass(fake_uncert1, unit=u.cm)
    assert_array_equal(fake_uncert2.array, uncert.value)
    assert (fake_uncert2.array is not uncert.value)
    assert (fake_uncert2.unit is u.cm)
