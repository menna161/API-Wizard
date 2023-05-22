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


def test_2d_trim(self):
    '\n        Test trimming of 2D array when size is not perfectly divisible\n        by block_size.\n        '
    data1 = np.arange(15).reshape(5, 3)
    result1 = block_reduce(data1, 2)
    data2 = data1[(0:4, 0:2)]
    result2 = block_reduce(data2, 2)
    assert np.all((result1 == result2))
