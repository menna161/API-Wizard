import numpy as np
from scipy.spatial import Delaunay
import astropy.io.fits as pyfits
import sklearn.neighbors
from . import observate
import pyfits


def weightsDT(self, target_points):
    'The interpolation weights are determined from barycenter\n        coordinates of the vertices of the enclosing Delaunay\n        triangulation simplex. This allows for the use of irregular Nd\n        grids. See also weights_1DLinear and\n        weights_kNN_inverse_distance.\n\n        :param target_points: ndarray, shape(ntarg,npar)\n            The coordinates to which you wish to interpolate.\n\n        :returns inds: ndarray, shape(ntarg,npar+1)\n             The model indices of the interpolates.\n\n        :returns weights: narray, shape (ntarg,npar+1)\n             The weights of each model given by ind in the\n             interpolates.\n        '
    ndim = target_points.shape[(- 1)]
    triangle_inds = self.dtri.find_simplex(target_points)
    inds = self.dtri.vertices[(triangle_inds, :)]
    tmp = self.dtri.transform[(triangle_inds, ndim, :)]
    bary = np.dot(self.dtri.transform[(triangle_inds, :ndim, :ndim)], (target_points - tmp).reshape((- 1), ndim, 1))
    oned = np.arange(triangle_inds.shape[0])
    bary = np.atleast_2d(np.squeeze(bary[(oned, :, oned, :)]))
    last = (1 - bary.sum(axis=(- 1)))
    weights = np.hstack((bary, last[(:, np.newaxis)]))
    outside = (triangle_inds == (- 1))
    weights[(outside, :)] = 0
    return (inds, weights)
