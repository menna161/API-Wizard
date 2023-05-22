import glob
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pickle
import warnings
from matplotlib import cm
from .lplot import *


def viewReps(prefix, label=[], val='Fit', title='Fitness', axis=False, getBest=False):
    (fig, ax) = getAxis(axis)
    fig.dpi = 100
    bestRun = []
    for pref in prefix:
        statFile = sorted(glob.glob((pref + '*stats.out')))
        if (len(statFile) == 0):
            print('ERROR: No files with that prefix found (it is a list?)')
            return False
        for i in range(len(statFile)):
            tmp = lload(statFile[i])
            if (i == 0):
                x = tmp[(:, 0)]
                if (val == 'Conn'):
                    fitVal = tmp[(:, 5)]
                else:
                    fitVal = tmp[(:, 3)]
                    bestVal = fitVal[(- 1)]
                    bestRun.append(statFile[i])
            else:
                if (np.shape(tmp)[0] != np.shape(fitVal)[0]):
                    print('Incomplete file found, ignoring ', statFile[i], ' and later.')
                    break
                if (val == 'Conn'):
                    fitVal = np.c_[(fitVal, tmp[(:, 5)])]
                else:
                    fitVal = np.c_[(fitVal, tmp[(:, 3)])]
                    if (fitVal[((- 1), (- 1))] > bestVal):
                        bestVal = fitVal[((- 1), (- 1))]
                        bestRun[(- 1)] = statFile[i]
        x = np.arange(len(x))
        lquart(x, fitVal, axis=ax)
    if (len(label) > 0):
        newLeg = []
        for i in range(len(label)):
            newLeg.append(label[i])
            newLeg.append('_nolegend_')
            newLeg.append('_nolegend_')
        warnings.filterwarnings('ignore', category=UserWarning)
        plt.gca().legend(newLeg)
    plt.title(title)
    plt.xlabel('Evaluations')
    plt.xlabel('Generations')
    if (val == 'Conn'):
        plt.ylabel('Median Connections')
    else:
        plt.ylabel('Best Fitness Found')
    if (getBest is True):
        return (fig, ax, bestRun)
    else:
        return (fig, ax)
