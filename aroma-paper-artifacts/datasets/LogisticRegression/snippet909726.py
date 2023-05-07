import pdb, sys, os, random
import numpy as np
import warnings
import math
import copy
import pickle
import argparse
import functools
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from scipy.stats import ttest_ind
from StatTest import pbinom
from scipy.stats import ranksums
from scipy.stats import wilcoxon
from StatTest import HyperGeometricTest as HyperTest
from File import TabFile
from File import MotifFile
from File import FastaFile
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import Birch
from imblearn.over_sampling import SMOTE
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.decomposition import PCA
from KF2 import smootherMultiple
from KF2 import KalmanFilterInd
from ClusteringMetric import DBI, AIC, PhamFK
from scipy.spatial.distance import pdist, squareform
from viz import viz
import gc
import pkg_resources


def getTransition(self, dTD, dTG, dMb, FCUT=1):
    G = self.getFC()
    dFC = {item[0].upper(): item[1] for item in G}
    etfID = [item[1] for item in self.etf]
    HGL = [item.upper() for item in self.GL]
    dR = {0: 2, 1: (- 2), 2: 0}
    try:
        [X, Y, U, D] = buildTrain(G, dTG, etfID, self.GL, FCUT)
        dR = {0: U, 1: D, 2: 0}
        LR = LogisticRegressionCV(penalty='l1', Cs=[1.5, 2, 3, 4, 5], solver='liblinear', multi_class='ovr')
        LR.fit(X, Y)
        CE = LR.coef_
        petf = parseLR(self.etf, CE)
        XX = []
        for i in HGL:
            if (i in dTG):
                tfi = dTG[i]
                xi = [(1 if (item in tfi) else 0) for item in etfID]
            else:
                xi = ([0] * len(etfID))
            XX.append(xi)
        YY = LR.predict(XX)
        self.etf = petf
    except:
        YY = [(0 if (dFC[item] > FCUT) else (1 if (dFC[item] < ((- 1) * FCUT)) else 2)) for item in HGL]
    YY = [dR[item] for item in YY]
    return YY
