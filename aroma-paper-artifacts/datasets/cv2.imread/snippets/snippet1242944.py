import numpy as np
import cv2
import os
import h5py
import scipy.io
import math
import skimage
from Demosaicing_malvar2004 import demosaicing_CFA_Bayer_Malvar2004
import random
import pyximport
from tone_mapping_cython import CRF_Map_Cython, ICRF_Map_Cython
import time
import matplotlib.pyplot as plt

if (__name__ == '__main__'):
    isp = ISP('./')
    path = './01_gt.png'
    img = cv2.imread(path)[(:, :, ::(- 1))]
    np.array(img, dtype='uint8')
    img = (img.astype('double') / 255.0)
    print('ISP test step by step:')
    img_L = isp.ICRF_Map(img, index=10)
    img_XYZ = isp.RGB2XYZ(img_L)
    xyz2cam = np.array([1.0234, (- 0.2969), (- 0.2266), (- 0.5625), 1.6328, (- 0.0469), (- 0.0703), 0.2188, 0.6406])
    img_Cam = isp.XYZ2CAM(img_XYZ, xyz2cam)
    img_mosaic = isp.mosaic_bayer(img_Cam)
    img_mosaic_noise = isp.add_PG_noise(img_mosaic)
    img_demosaic = isp.Demosaic(img_mosaic_noise)
    img_IXYZ = isp.CAM2XYZ(img_demosaic, xyz2cam)
    img_IL = isp.XYZ2RGB(img_IXYZ)
    img_Irgb = isp.CRF_Map(img_IL, index=10)
    fig = plt.figure(0)
    fig.canvas.set_window_title('Step test')
    plt.imshow(img_Irgb)
    print('ISP test on sRGB space:')
    (im_gt, im_noisy) = isp.cbdnet_noise_generate_srgb(img)
    fig = plt.figure(1)
    fig.canvas.set_window_title('sRGB')
    plt.imshow(np.concatenate((im_gt, im_noisy), axis=1))
    plt.show()
