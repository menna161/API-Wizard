from chainer_compiler.elichika import testtools
import argparse
import pickle
import sys
import os
import chainer
import chainer.functions as F
from chainer.backends import cuda
import numpy as np


def main():
    x = np.arange((((2 * 3) * 5) * 5)).reshape((2, 3, 5, 5)).astype(np.float32)
    rois = np.array([[0, 1, 3, 4], [1, 0.3, 4, 2.6]]).astype(np.float32)
    roi_indices = np.array([0, 1]).astype(np.int32)
    testtools.generate_testcase(ROIPool2D(F.roi_max_pooling_2d, 7, 1.2), [x, rois, roi_indices], subname='max_pool')
    testtools.generate_testcase(ROIPool2D(F.roi_average_pooling_2d, 7, 1.2), [x, rois, roi_indices], subname='avg_pool')
    testtools.generate_testcase(ROIAlign2D(F.roi_max_align_2d, 7, 1.2, 2), [x, rois, roi_indices], subname='max_align')
    testtools.generate_testcase(ROIAlign2D(F.roi_average_align_2d, 7, 1.2, 3), [x, rois, roi_indices], subname='avg_align')
