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


def discrete_matshow(data):
    data = data.astype(np.int64)
    cmap = plt.get_cmap('tab20', ((np.max(data) - np.min(data)) + 1))
    mat = plt.matshow(data, cmap=cmap, vmin=(np.min(data) - 0.5), vmax=(np.max(data) + 0.5))
    cax = plt.colorbar(mat, ticks=np.arange(np.min(data), (np.max(data) + 1)))
    cax.ax.set_yticklabels(labels)
