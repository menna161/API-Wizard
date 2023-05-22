import textwrap
import numpy as np
import pytest
from astropy.io import fits
from astropy.nddata.nduncertainty import StdDevUncertainty, MissingDataAssociationException, VarianceUncertainty, InverseVariance
from astropy import units as u
from astropy import log
from astropy.wcs import WCS, FITSFixedWarning
from astropy.tests.helper import catch_warnings
from astropy.utils import NumpyRNGContext
from astropy.utils.data import get_pkg_data_filename, get_pkg_data_filenames, get_pkg_data_contents
from astropy.utils.exceptions import AstropyWarning
from astropy.nddata.ccddata import CCDData
from astropy.nddata import _testing as nd_testing
from astropy.table import Table
from astropy.nddata.ccddata import _KEEP_THESE_KEYWORDS_IN_HEADER
from astropy.nddata.ccddata import _generate_wcs_and_update_header
from astropy.nddata.ccddata import _KEEP_THESE_KEYWORDS_IN_HEADER, _CDs, _PCs


def test_arithmetic_add_with_array():
    ccd = CCDData(np.ones((3, 3)), unit='')
    res = ccd.add(np.arange(3))
    np.testing.assert_array_equal(res.data, ([[1, 2, 3]] * 3))
    ccd = CCDData(np.ones((3, 3)), unit='adu')
    with pytest.raises(ValueError):
        ccd.add(np.arange(3))
