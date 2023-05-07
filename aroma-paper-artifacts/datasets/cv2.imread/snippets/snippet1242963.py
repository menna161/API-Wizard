import numpy as np
import cv2
import os
import h5py
import scipy.io
import math
import skimage
from Demosaicing_malvar2004 import demosaicing_CFA_Bayer_Malvar2004
import random

if (__name__ == '__main__'):
    isp = ISP()
    path = './figs/01_gt.png'
    img = cv2.imread(path)
    np.array(img, dtype='uint8')
    img = (img.astype('double') / 255.0)
    img_rgb = isp.BGR2RGB(img)
    "\n    print('ISP test 1:')\n    # -------- INVERSE ISP PROCESS -------------------\n    # Step 1 : inverse tone mapping\n    img_L = isp.ICRF_Map(img_rgb, index=10)\n    # Step 2 : from RGB to XYZ\n    img_XYZ = isp.RGB2XYZ(img_L)\n    # Step 3: from XYZ to Cam\n    xyz2cam = np.array([1.0234, -0.2969, -0.2266, -0.5625, 1.6328, -0.0469, -0.0703, 0.2188, 0.6406])\n    img_Cam = isp.XYZ2CAM(img_XYZ, xyz2cam)\n    # Step 4: Mosaic\n    img_mosaic = isp.mosaic_bayer(img_Cam)\n\n    # -------- ADDING POISSON-GAUSSIAN NOISE ON RAW -\n    # Mode1: set sigma_s and sigma_c\n    # img_mosaic_noise = isp.add_PG_noise(img_mosaic, sigma_s=0.01, sigma_c=0.02)\n    # Mode2: set random sigma_s and sigma_c\n    img_mosaic_noise = isp.add_PG_noise(img_mosaic)\n\n    # -------- ISP PROCESS --------------------------\n    # Step 4 : Demosaic\n    img_demosaic = isp.Demosaic(img_mosaic_noise)\n    # Step 3 : from Cam to XYZ\n    img_IXYZ = isp.CAM2XYZ(img_demosaic, xyz2cam)\n    # Step 2 : frome XYZ to RGB\n    img_IL = isp.XYZ2RGB(img_IXYZ)\n    # Step 1 : tone mapping\n    img_Irgb = isp.CRF_Map(img_IL, index=10)\n    "
    "\n    # Observe the images\n    show_img = np.concatenate((img,\n                               isp.RGB2BGR(img_Irgb),\n                               cv2.merge([img_mosaic, img_mosaic, img_mosaic]),\n                               isp.RGB2BGR(img_demosaic)\n                               ), axis=1)\n    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)\n    cv2.imshow('Image', show_img)\n    cv2.waitKey(0)\n    "
    "\n    print('ISP test 2:')\n    gt, noise = isp.cbdnet_noise_generate_srgb(img_rgb)\n\n    # Observe the images\n    show_img = np.concatenate((img,\n                               isp.RGB2BGR(gt),\n                               isp.RGB2BGR(noise)\n                               ), axis=1)\n    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)\n    cv2.imshow('Image', show_img)\n    cv2.waitKey(0)\n    "
    print('ISP test 3:')
    (gt, noise) = isp.cbdnet_noise_generate_raw(img_rgb)
    print(noise_map)
    show_img = np.concatenate((img, cv2.merge([(noise_map / 255), (noise_map / 255), (noise_map / 255)]), cv2.merge([noise, noise, noise])), axis=1)
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', show_img)
    cv2.waitKey(0)
    "\n    img_Ibgr = isp.RGB2BGR(img_Irgb)\n    cv2.imwrite('./figs/01_inverse.png', img_Ibgr*255)\n    "
