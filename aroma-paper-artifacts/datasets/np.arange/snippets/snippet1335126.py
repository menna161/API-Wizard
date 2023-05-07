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


def test_extract_array_1d_trim():
    'Extract 1 d arrays.\n\n    All dimensions are treated the same, so we can test in 1 dim.\n    '
    assert np.all((extract_array(np.arange(4), (2,), (0,), mode='trim') == np.array([0])))
    for i in [1, 2, 3]:
        assert np.all((extract_array(np.arange(4), (2,), (i,), mode='trim') == np.array([(i - 1), i])))
    assert np.all((extract_array(np.arange(4.0), (2,), (4,), mode='trim') == np.array([3])))
