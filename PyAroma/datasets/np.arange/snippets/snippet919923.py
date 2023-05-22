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


def GroundTruthVisualise(data, dataset, original=True):
    from matplotlib.pyplot import imshow, show, colorbar, set_cmap, clim
    import matplotlib.pyplot as plt
    import numpy as np
    labels = []
    if (dataset == 'Indian_pines'):
        if original:
            labels = ['Unlabelled', 'Corn-notil', 'Corn-mintill', 'Corn', 'Grass-pasture', 'Grass-trees', 'Hay-windrowed', 'Soybean-notil', 'Soybean-mintil', 'Soybean-clean', 'Woods', 'BGTD']
        else:
            labels = []
    elif (dataset == 'Salinas'):
        labels = ['Unlabelled', 'Brocoli green weeds 1', 'Brocoli green weeds 2', 'Fallow', 'Fallow rough plow', 'Fallow smooth', 'Stubble', 'Celery', 'Grapes untrained', 'Soil vinyard develop', 'Corn senesced green weeds', 'Lettuce romaine 4wk', 'Lettuce romaine 5wk', 'Lettuce romaine 6wk', 'Lettuce romaine 7wk', 'Vinyard untrained', 'Vunyard vertical trellis']
    elif (dataset == 'KSC'):
        labels = ['Unlabelled', 'Scrub', 'Williw swamp', 'SP hammock', 'Slash pine', 'Oak/Broadleaf', 'Hardwood', 'Swamp', 'Gramminoid marsh', 'Spartina marsh', 'Cattail marsh', 'Salt marsh', 'Mud flats', 'Water']

    def discrete_matshow(data):
        data = data.astype(np.int64)
        cmap = plt.get_cmap('tab20', ((np.max(data) - np.min(data)) + 1))
        mat = plt.matshow(data, cmap=cmap, vmin=(np.min(data) - 0.5), vmax=(np.max(data) + 0.5))
        cax = plt.colorbar(mat, ticks=np.arange(np.min(data), (np.max(data) + 1)))
        cax.ax.set_yticklabels(labels)
    imshow(data)
    discrete_matshow(data)
    show()
