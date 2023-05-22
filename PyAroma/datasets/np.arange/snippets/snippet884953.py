import sys, os, glob
import subprocess
import numpy as np
from . import photometer
from astropy import wcs as pywcs
import astropy.io.fits as pyfits
import pyfits


def __init__(self, imagename):
    self.image_name = imagename
    self.image = pyfits.getdata(imagename)
    self.header = pyfits.getheader(imagename)
    self.wcs = pywcs.WCS(self.header)
    try:
        self.plate_scale = (3600.0 * np.sqrt((self.wcs.wcs.cd ** 2).sum(axis=1)))
    except AttributeError:
        self.plate_scale = (3600.0 * np.abs(self.wcs.wcs.cdelt))
    self.mask = np.ones_like(self.image, dtype=bool)
    (ny, nx) = self.mask.shape
    (self.y, self.x) = np.meshgrid(np.arange(ny), np.arange(nx))
