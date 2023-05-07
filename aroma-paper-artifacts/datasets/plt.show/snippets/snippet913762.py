import cv2
import numpy as np
import chainer.links as L
from chainer_bcnn.links.connection import Convolution2D
from chainer_bcnn.links.connection import Deconvolution2D
from chainer_bcnn.initializers import BilinearUpsample
from chainer_bcnn.functions import crop
import matplotlib.pyplot as plt


def test_compare_model(x, model_1, model_2):
    print('x.shape:', x.shape)
    y_1 = model_1(x).data
    y_2 = model_2(x).data
    y_2 = crop(y_2, y_1.shape, ndim=2)
    print('y_1.shape:', y_1.shape)
    print('y_2.shape:', y_2.shape)
    plt.subplot(141)
    plt.imshow(x[(0, 0, :, :)], cmap='gray')
    plt.colorbar()
    plt.subplot(142)
    plt.imshow(y_1[(0, 0, :, :)], cmap='gray')
    plt.colorbar()
    plt.subplot(143)
    plt.imshow(y_2[(0, 0, :, :)], cmap='gray')
    plt.colorbar()
    plt.subplot(144)
    plt.imshow(np.abs((y_2[(0, 0, :, :)] - y_1[(0, 0, :, :)])), cmap='jet')
    plt.colorbar()
    plt.show()
