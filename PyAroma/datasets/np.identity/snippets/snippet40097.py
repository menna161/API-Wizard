import tifffile
import glob
import cv2
import numpy as np
import numpy.linalg as la
import cv2 as cv
from osgeo import gdal
import os
import math
from skimage import img_as_ubyte
from copy import deepcopy
import epipolar
from rpc import RPC
from utm import *
from model_icnet import build_icnet
from densemapnet import DenseMapNet
from densemapnet import Settings


def stereo_to_xyz(img1_name, img2_name, predictor):
    img1 = cv2.imread(img1_name, 0)
    img2 = cv2.imread(img2_name, 0)
    rgb_img1 = tifffile.imread(img1_name)
    rgb_img2 = tifffile.imread(img2_name)
    rpc1 = RPC(img1_name)
    rpc2 = RPC(img2_name)
    rows = img1.shape[0]
    cols = img1.shape[1]
    (F, pts1, pts2) = match_rpc(rpc1, rpc2, rows, cols)
    x1 = pts1.T
    x2 = pts2.T
    d = None
    K = np.identity(3)
    (rimg1, rimg2, rms, max_error, lH, rH, max_yparallax) = rectify_images(img1, x1, img2, x2, K, d, F, shearing=False)
    print('F Matrix Residual RMS Error = ', rms, ' pixels')
    print('F Matrix Residual Max Error = ', max_error, ' pixels')
    if (rms > 1.0):
        return (None, None, None, None, None)
    if (max_yparallax > 2.0):
        return (None, None, None, None, None)
    rows = img1.shape[0]
    cols = img1.shape[1]
    row_offset = int((rows / 4))
    col_offset = int((cols / 4))
    (rgb_rimg1, rgb_rimg2, rgb_rms, rgb_max_error) = rectify_images_rgb(rgb_img1, x1, rgb_img2, x2, K, d, F, shearing=False)
    rimg1 = rgb_rimg1[(row_offset:(rows - row_offset), col_offset:(cols - col_offset), :)]
    rimg2 = rgb_rimg2[(row_offset:(rows - row_offset), col_offset:(cols - col_offset), :)]
    if USE_SGM:
        disparity = sgbm(rimg1, rimg2)
    else:
        disparity = predictor.predict_stereo(rimg1, rimg2)
    seg_rimg1 = predictor.predict_semantics(rimg1)
    rows = rimg1.shape[0]
    cols = rimg1.shape[1]
    valid = np.ones((rows, cols), dtype=bool)
    valid[(disparity < (- DMAX_SEARCH))] = 0
    valid[(disparity > DMAX_SEARCH)] = 0
    disparity[(disparity < (- DMAX_SEARCH))] = (- DMAX_SEARCH)
    disparity[(disparity > DMAX_SEARCH)] = DMAX_SEARCH
    print('Min disparity found: ', disparity.min())
    print('Max disparity found: ', disparity.max())
    disparity_image = ((disparity + DMAX_SEARCH) / (DMAX_SEARCH * 2.0))
    disparity_image[(disparity_image < 0.0)] = 0.0
    disparity_image = img_as_ubyte(disparity_image)
    cls_image = category_to_color(seg_rimg1)
    rows = rimg1.shape[0]
    cols = rimg1.shape[1]
    (left_rows, left_cols) = np.mgrid[(row_offset:(rows + row_offset), col_offset:(cols + col_offset))]
    right_cols = (deepcopy(left_cols) - disparity)
    right_rows = deepcopy(left_rows)
    valid[(right_cols < col_offset)] = 0
    valid[(right_cols > ((cols + col_offset) - 1))] = 0
    left_rows = left_rows.ravel()
    left_cols = left_cols.ravel()
    right_rows = right_rows.ravel()
    right_cols = right_cols.ravel()
    num = len(left_cols)
    print('left cols = ', num)
    uv1 = np.array((left_cols, left_rows, np.ones(num)))
    print(uv1.shape)
    print(rH.shape)
    xyw = np.matmul(np.linalg.inv(rH), uv1)
    left_cols = (xyw[0] / xyw[2])
    left_rows = (xyw[1] / xyw[2])
    uv2 = np.array((right_cols, right_rows, np.ones(num)))
    xyw = np.matmul(np.linalg.inv(lH), uv2)
    right_cols = (xyw[0] / xyw[2])
    right_rows = (xyw[1] / xyw[2])
    left_seg = seg_rimg1
    print('left_seg shape = ', left_seg.shape)
    left_seg = left_seg.ravel()
    print('valid shape = ', valid.shape)
    valid = valid.ravel()
    print('valid shape = ', valid.shape)
    (clat, clon, zc) = rpc1.approximate_wgs84()
    (xc, yc, zone_number, zone_letter) = wgs84_to_utm(clat, clon)
    (R1, rms1, ic1, jc1) = rpc1.to_matrix(clat, clon, zc)
    (R2, rms2, ic2, jc2) = rpc2.to_matrix(clat, clon, zc)
    print('Triangulating...')
    points1 = np.array(((left_cols - ic1), (left_rows - jc1)))
    points2 = np.array(((right_cols - ic2), (right_rows - jc2)))
    xyz = cv2.triangulatePoints(R1, R2, points1, points2)
    xyz /= xyz[3]
    xyz = xyz[(0:3, valid)]
    xyz[(0, :)] += xc
    xyz[(1, :)] += yc
    xyz[(2, :)] += zc
    xyz = np.transpose(xyz)
    print(zone_number, zone_letter)
    xyzc = np.zeros((xyz.shape[0], (xyz.shape[1] + 1)))
    xyzc[(:, 0:3)] = xyz
    left_seg = left_seg[valid]
    xyzc[(:, 3)] = left_seg
    return (xyzc, rimg1, rimg2, disparity_image, cls_image)
