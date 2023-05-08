import cv2
import numpy as np
import chainer.links as L
from chainer_bcnn.links.connection import Convolution2D
from chainer_bcnn.links.connection import Deconvolution2D
from chainer_bcnn.initializers import BilinearUpsample
from chainer_bcnn.functions import crop
import matplotlib.pyplot as plt


def main():
    x = cv2.imread('lenna.png')
    x = cv2.resize(x, (64, 64))
    x = np.transpose(x, (2, 0, 1))
    x = np.expand_dims(x, axis=0).astype(np.float32)
    c = x.shape[1]
    conv_default = L.Convolution2D(c, c, ksize=(3, 3), stride=1, pad=(1, 1), initialW=BilinearUpsample(), nobias=True)
    conv_reflect = Convolution2D(c, c, ksize=(3, 3), stride=1, pad=(1, 1), initialW=BilinearUpsample(), nobias=True)
    deconv_default = L.Deconvolution2D(c, c, ksize=(3, 3), stride=2, pad=(0, 0), initialW=BilinearUpsample(), nobias=True)
    deconv_reflect = Deconvolution2D(c, c, ksize=(3, 3), stride=2, pad=(1, 1), initialW=BilinearUpsample(), nobias=True)
    test_compare_model(x, conv_default, conv_reflect)
    test_compare_model(x, deconv_default, deconv_reflect)
