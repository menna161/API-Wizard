import numpy as np
import time
import sys
import random
from domain.make_env import make_env
from .ind import *


def getDistFitness(self, wVec, aVec, hyp, seed=(- 1), nRep=False, nVals=6, view=False, returnVals=False):
    "Get fitness of a single individual with distribution of weights\n  \n    Args:\n      wVec    - (np_array) - weight matrix as a flattened vector\n                [N**2 X 1]\n      aVec    - (np_array) - activation function of each node \n                [N X 1]    - stored as ints (see applyAct in ann.py)\n      hyp     - (dict)     - hyperparameters\n        ['alg_wDist']        - weight distribution  [standard;fixed;linspace]\n        ['alg_absWCap']      - absolute value of highest weight for linspace\n  \n    Optional:\n      seed    - (int)      - starting random seed for trials\n      nReps   - (int)      - number of trials to get average fitness\n      nVals   - (int)      - number of weight values to test\n\n  \n    Returns:\n      fitness - (float)    - mean reward over all trials\n    "
    if (nRep is False):
        nRep = hyp['alg_nReps']
    if ((hyp['alg_wDist'] == 'standard') and (nVals == 6)):
        wVals = np.array(((- 2), (- 1.0), (- 0.5), 0.5, 1.0, 2))
    else:
        wVals = np.linspace((- self.absWCap), self.absWCap, nVals)
    reward = np.empty((nRep, nVals))
    for iRep in range(nRep):
        for iVal in range(nVals):
            wMat = self.setWeights(wVec, wVals[iVal])
            if (seed == (- 1)):
                reward[(iRep, iVal)] = self.testInd(wMat, aVec, seed=seed, view=view)
            else:
                reward[(iRep, iVal)] = self.testInd(wMat, aVec, seed=(seed + iRep), view=view)
    if (returnVals is True):
        return (np.mean(reward, axis=0), wVals)
    return np.mean(reward, axis=0)
