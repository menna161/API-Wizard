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


def test_extract_array_wrong_mode():
    'Call extract_array with non-existing mode.'
    with pytest.raises(ValueError) as e:
        extract_array(np.arange(4), (2,), (0,), mode='full')
    assert ("Valid modes are 'partial', 'trim', and 'strict'." == str(e.value))
