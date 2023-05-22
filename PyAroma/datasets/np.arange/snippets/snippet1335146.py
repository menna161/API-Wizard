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


def setup_class(self):
    self.data = np.arange(20.0).reshape(5, 4)
    self.position = SkyCoord('13h11m29.96s -01d19m18.7s', frame='icrs')
    wcs = WCS(naxis=2)
    rho = (np.pi / 3.0)
    scale = (0.05 / 3600.0)
    wcs.wcs.cd = [[(scale * np.cos(rho)), ((- scale) * np.sin(rho))], [(scale * np.sin(rho)), (scale * np.cos(rho))]]
    wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN']
    wcs.wcs.crval = [self.position.ra.to_value(u.deg), self.position.dec.to_value(u.deg)]
    wcs.wcs.crpix = [3, 3]
    self.wcs = wcs
    sipwcs = wcs.deepcopy()
    sipwcs.wcs.ctype = ['RA---TAN-SIP', 'DEC--TAN-SIP']
    a = np.array([[0, 0, 5.33092692e-08, 3.73753773e-11, (- 2.02111473e-13)], [0, 2.44084308e-05, 2.81394789e-11, 5.17856895e-13, 0.0], [(- 2.41334657e-07), 1.29289255e-10, 2.35753629e-14, 0.0, 0.0], [(- 2.37162007e-10), 5.43714947e-13, 0.0, 0.0, 0.0], [(- 2.81029767e-13), 0.0, 0.0, 0.0, 0.0]])
    b = np.array([[0, 0, 2.99270374e-05, (- 2.38136074e-10), 7.23205168e-13], [0, (- 1.71073858e-07), 6.31243431e-11, (- 5.16744347e-14), 0.0], [6.95458963e-06, (- 3.08278961e-10), (- 1.75800917e-13), 0.0, 0.0], [3.51974159e-11, 5.60993016e-14, 0.0, 0.0, 0.0], [(- 5.92438525e-13), 0.0, 0.0, 0.0, 0.0]])
    sipwcs.sip = Sip(a, b, None, None, wcs.wcs.crpix)
    sipwcs.wcs.set()
    self.sipwcs = sipwcs
