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


def test_2d_conserve_sum(self):
    'Test 2D array with conserve_sum=False.'
    data = np.arange(6).reshape(2, 3)
    block_size = 2.0
    expected = (block_replicate(data, block_size) * (block_size ** 2))
    result = block_replicate(data, block_size, conserve_sum=False)
    assert np.all((result == expected))