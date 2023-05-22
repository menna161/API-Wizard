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


def test_initialize_from_fits_with_data_in_different_extension(tmpdir):
    fake_img = np.arange(4).reshape(2, 2)
    hdu1 = fits.PrimaryHDU()
    hdu2 = fits.ImageHDU(fake_img)
    hdus = fits.HDUList([hdu1, hdu2])
    filename = tmpdir.join('afile.fits').strpath
    hdus.writeto(filename)
    with catch_warnings(FITSFixedWarning) as w:
        ccd = CCDData.read(filename, unit='adu')
    assert (len(w) == 0)
    np.testing.assert_array_equal(ccd.data, fake_img)
    assert ((hdu2.header + hdu1.header) == ccd.header)
