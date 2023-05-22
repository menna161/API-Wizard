from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import itertools
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import KFold, LeaveOneOut, RepeatedKFold, ShuffleSplit
import deepxde as dde
from data import BerkovichData, ExpData, FEMData, ModelData
from mfgp import LinearMFGP


def nn(data):
    layer_size = (([data.train_x.shape[1]] + ([32] * 2)) + [1])
    activation = 'selu'
    initializer = 'LeCun normal'
    regularization = ['l2', 0.01]
    loss = 'MAPE'
    optimizer = 'adam'
    if (data.train_x.shape[1] == 3):
        lr = 0.0001
    else:
        lr = 0.001
    epochs = 30000
    net = dde.maps.FNN(layer_size, activation, initializer, regularization=regularization)
    model = dde.Model(data, net)
    model.compile(optimizer, lr=lr, loss=loss, metrics=['MAPE'])
    (losshistory, train_state) = model.train(epochs=epochs)
    dde.saveplot(losshistory, train_state, issave=True, isplot=False)
    return train_state.best_metrics[0]
