import random
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from multiprocessing import Pool
from fancyimpute import MICE
import scipy
import scipy.sparse
import scipy.sparse.linalg
import numpy as np
import json
import sys
import time
import os
import utils


def rfe_multiprocess(i, dets, deform, body_num, x, measure, k_features):
    sys.stdout.write(('>> calc rfe map NO.%d\n' % i))
    y = np.array(dets).reshape(body_num, 1)
    model = LinearRegression()
    rfe = RFE(model, k_features)
    rfe.fit(x, y.ravel())
    flag = np.array(rfe.support_).reshape(utils.M_NUM, 1)
    flag = flag.repeat(body_num, axis=1)
    S = np.array(deform)
    S.shape = (S.size, 1)
    m = np.array(measure[flag])
    m.shape = (k_features, body_num)
    M = build_equation(m, 9)
    MtM = M.transpose().dot(M)
    MtS = M.transpose().dot(S)
    ans = np.array(scipy.sparse.linalg.spsolve(MtM, MtS))
    ans.shape = (9, k_features)
    return [ans, rfe.support_]
