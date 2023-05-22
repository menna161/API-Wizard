from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
import os, sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn import metrics
from scipy import interp
import random
import numpy as np


def load_data_TF2(indel_list, data_path):
    import random
    import numpy as np
    xxdata_list = []
    yydata = []
    count_set = [0]
    count_setx = 0
    for i in indel_list:
        xdata = np.load((((data_path + '/Nxdata_tf') + str(i)) + '.npy'))
        ydata = np.load((((data_path + '/ydata_tf') + str(i)) + '.npy'))
        for k in range(len(ydata)):
            xxdata_list.append(xdata[(k, :, :, :)])
            yydata.append(ydata[k])
        count_setx = (count_setx + len(ydata))
        count_set.append(count_setx)
        print(i, len(ydata))
    yydata_array = np.array(yydata)
    yydata_x = yydata_array.astype('int')
    print(np.array(xxdata_list).shape)
    return (np.array(xxdata_list), yydata_x, count_set)
