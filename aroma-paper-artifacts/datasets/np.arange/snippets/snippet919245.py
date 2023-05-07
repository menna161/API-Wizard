import numpy as np
from sphericalpolygon import create_polygon
from pyshtools.spectralanalysis import Curve2Mask
from ..ggclasses.class_Nodes import Nodes


def yx2latlon(lats_region, lons_region, yx):
    '\n    Transform index to latitudes and longitudes.\n \n    Usage: \n    latlon = yx2latlon(lats_region,lons_region,yx)\n \n    Inputs:\n    lats_region -> [float array] latitudes of a region\n    lons_region -> [float array] longitudes of a region\n    yx -> [float 2d arrays] index of points in the form of [[y0,x0],..[yn,xn]]; note that the y coordinates are counted from top to bottom;\n \n    Outputs:\n    latlon -> [float arrays] latitudes and longitudes in the form of [[lat0,lon0],..[latn,lonn]]\n\n    Example:\n    >>> lats_region = np.arange(20,50)\n    >>> lons_region = np.arange(70,110)\n    >>> yx = np.array([[1,2],[13,17],[24,36]])\n    >>> latlon = yx2latlon(lats_region,lons_region,yx)\n    >>> print(latlon)\n    [[ 21  72]\n     [ 33  87]\n    [ 44 106]]\n    '
    (ys, xs) = (yx[(:, 0)], yx[(:, 1)])
    (step_lats, step_lons) = ((lats_region[1] - lats_region[0]), (lons_region[1] - lons_region[0]))
    lats = (lats_region[0] + (ys * step_lats))
    lons = (lons_region[0] + (xs * step_lons))
    return np.stack((lats, lons), axis=1)
