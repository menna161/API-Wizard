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


def mfnn(data):
    (x_dim, y_dim) = (3, 1)
    activation = 'selu'
    initializer = 'LeCun normal'
    regularization = ['l2', 0.01]
    net = dde.maps.MfNN((([x_dim] + ([128] * 2)) + [y_dim]), (([8] * 2) + [y_dim]), activation, initializer, regularization=regularization, residue=True, trainable_low_fidelity=True, trainable_high_fidelity=True)
    model = dde.Model(data, net)
    model.compile('adam', lr=0.0001, loss='MAPE', metrics=['MAPE', 'APE SD'])
    (losshistory, train_state) = model.train(epochs=30000)
    dde.saveplot(losshistory, train_state, issave=True, isplot=False)
    return (train_state.best_metrics[1], train_state.best_metrics[3], train_state.best_y[1])
