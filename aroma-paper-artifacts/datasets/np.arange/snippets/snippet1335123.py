import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from astropy.tests.helper import assert_quantity_allclose
from astropy.nddata.utils import extract_array, add_array, subpixel_indices, block_reduce, block_replicate, overlap_slices, NoOverlapError, PartialOverlapError, Cutout2D
from astropy.wcs import WCS, Sip
from astropy.wcs.utils import proj_plane_pixel_area
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.nddata import CCDData
import skimage


def test_extract_array_1d_odd():
    'Extract 1 d arrays.\n\n    All dimensions are treated the same, so we can test in 1 dim.\n    The first few lines test the most error-prone part: Extraction of an\n    array on the boundaries.\n    Additional tests (e.g. dtype of return array) are done for the last\n    case only.\n    '
    assert np.all((extract_array(np.arange(4), (3,), ((- 1),), fill_value=(- 99)) == np.array([(- 99), (- 99), 0])))
    assert np.all((extract_array(np.arange(4), (3,), (0,), fill_value=(- 99)) == np.array([(- 99), 0, 1])))
    for i in [1, 2]:
        assert np.all((extract_array(np.arange(4), (3,), (i,)) == np.array([(i - 1), i, (i + 1)])))
    assert np.all((extract_array(np.arange(4), (3,), (3,), fill_value=(- 99)) == np.array([2, 3, (- 99)])))
    arrayin = np.arange(4.0)
    extracted = extract_array(arrayin, (3,), (4,))
    assert (extracted[0] == 3)
    assert np.isnan(extracted[1])
    assert (extracted.dtype == arrayin.dtype)
