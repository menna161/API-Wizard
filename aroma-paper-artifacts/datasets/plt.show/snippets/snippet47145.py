import numpy as np
from astropy.io import fits
import os
from dps.datasets.base import ImageDataset, ImageFeature, VariableShapeArrayFeature, ArrayFeature, StringFeature
from dps.utils import Param, atleast_nd, walk_images
import tensorflow as tf
import matplotlib.pyplot as plt
from astropy.utils.data import get_pkg_data_filename

if (__name__ == '__main__'):
    import tensorflow as tf
    import matplotlib.pyplot as plt
    from astropy.utils.data import get_pkg_data_filename
    image_file = '/home/eric/Downloads/abell_2744_RGB.fits'
    image_data = fits.getdata(image_file, ext=0)
    plt.figure()
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()
    plt.show()
    n = 32
    dset = FITSDataset(fits_file=image_file, postprocessing='tile_pad', n_samples_per_image=n, tile_shape=(1000, 1000), force_memmap=False)
    print(dset.depth)
    sess = tf.Session()
    with sess.as_default():
        dset.visualize(n)
