import scipy.io
import scipy.io as io
import os
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from numpy import array
from random import shuffle
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import mean, argmax
from matplotlib.pyplot import imshow, show, colorbar, set_cmap, clim
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import imshow, show, subplots, axis, figure
import pandas as pd
from tensorflow.python.client import device_lib


def plot_random_spec_img(pic, true_label):
    '\n    Take first hyperspectral image from dataset and plot spectral data distribution\n    Arguements pic = list of images in size (?, height, width, bands), where ? represents any number > 0\n                true_labels = lists of ground truth corrospond to pic\n    '
    pic = pic[0]
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from numpy import mean, argmax
    print(('Image Shape: ' + str(pic.shape)))
    print(('Label of this image is -> ' + str(true_label[0])))
    title = argmax(true_label[0], axis=0)
    mean_value = mean(pic)
    pic[(pic < mean_value)] = 0
    x = []
    y = []
    z = []
    for z1 in range(pic.shape[0]):
        for x1 in range(pic.shape[1]):
            for y1 in range(pic.shape[2]):
                if (pic[(z1, x1, y1)] != 0):
                    z.append(z1)
                    x.append(x1)
                    y.append(y1)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(('True class = ' + str(title)))
    ax.scatter(x, y, z, color='#0606aa', marker='o', s=0.5)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Spectral Label')
    ax.set_zlabel('Y Label')
    plt.show()
