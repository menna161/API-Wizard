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


def test_extract_array_return_pos():
    "Check that the return position is calculated correctly.\n\n    The result will differ by mode. All test here are done in 1d because it's\n    easier to construct correct test cases.\n    "
    large_test_array = np.arange(5)
    for i in np.arange((- 1), 6):
        (extracted, new_pos) = extract_array(large_test_array, 3, i, mode='partial', return_position=True)
        assert (new_pos == (1,))
    for (i, expected) in zip([1.49, 1.51, 3], [0.49, 0.51, 1]):
        (extracted, new_pos) = extract_array(large_test_array, (2,), (i,), mode='strict', return_position=True)
        assert (new_pos == (expected,))
    for (i, expected) in zip(np.arange((- 1), 6), ((- 1), 0, 1, 1, 1, 1, 1)):
        (extracted, new_pos) = extract_array(large_test_array, (3,), (i,), mode='trim', return_position=True)
        assert (new_pos == (expected,))
