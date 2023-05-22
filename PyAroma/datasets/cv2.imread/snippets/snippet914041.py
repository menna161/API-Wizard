from __future__ import absolute_import
import numpy as np
import os
import cv2
from . import mhd


def load_image(filename):
    ' Load a two/three dimensional image from given filename\n\n    Args:\n        filename (str)\n\n    Returns:\n        numpy.ndarray: An image\n        list of float: Spacing\n    '
    (_, ext) = os.path.splitext(os.path.basename(filename))
    if (ext in ('.mha', '.mhd')):
        [img, img_header] = mhd.read(filename)
        spacing = img_header['ElementSpacing']
        img.flags.writeable = True
        if (img.ndim == 3):
            img = np.transpose(img, (1, 2, 0))
    elif (ext in ('.png', '.jpg', '.bmp')):
        img = cv2.imread(filename)
        spacing = None
    else:
        raise NotImplementedError()
    return (img, spacing)
