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


def test_extract_array_odd_shape_rounding():
    '\n    Test overlap_slices (via extract_array) for rounding with an\n    even-shaped extraction.\n    '
    data = np.arange(10)
    shape = (3,)
    positions_expected = [(1.49, (0, 1, 2)), (1.5, (0, 1, 2)), (1.501, (1, 2, 3)), (1.99, (1, 2, 3)), (2.0, (1, 2, 3)), (2.01, (1, 2, 3)), (2.49, (1, 2, 3)), (2.5, (1, 2, 3)), (2.501, (2, 3, 4)), (2.99, (2, 3, 4)), (3.0, (2, 3, 4)), (3.01, (2, 3, 4))]
    for (pos, exp) in positions_expected:
        out = extract_array(data, shape, (pos,), mode='partial')
        assert_array_equal(out, exp)
    positions = ((- 0.99), (- 0.51), (- 0.5), (- 0.49), (- 0.01), 0)
    exp1 = ((- 99), (- 99), 0)
    exp2 = ((- 99), 0, 1)
    expected = (([exp1] * 3) + ([exp2] * 4))
    for (pos, exp) in zip(positions, expected):
        out = extract_array(data, shape, (pos,), mode='partial', fill_value=(- 99))
        assert_array_equal(out, exp)
