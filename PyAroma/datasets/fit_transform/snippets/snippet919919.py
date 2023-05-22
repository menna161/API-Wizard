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


def OnehotTransform(labels):
    import numpy as np
    from sklearn.preprocessing import OneHotEncoder
    onehot_encoder = OneHotEncoder(sparse=False)
    labels = np.reshape(labels, (len(labels), 1))
    labels = onehot_encoder.fit_transform(labels).astype(np.uint8)
    return labels
