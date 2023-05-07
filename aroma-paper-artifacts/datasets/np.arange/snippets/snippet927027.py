import os
import sys
import time
import math
import argparse
import subprocess
import numpy as np
import cma
from neat_src import *
from domain import *
from mpi4py import MPI


def layer2mat(hyp, hLayers):
    ' \n  Creates weight matrix of fully connected layers\n\n  Example: layer2mat(hyp, [25,5]) # [input, [25x5] hidden, output]\n  '
    print('Layers: ', hLayers)
    nPerLay = (([(1 + hyp['ann_nInput'])] + hLayers) + [hyp['ann_nOutput']])
    nNodes = sum(nPerLay)
    adjMat = np.zeros((nNodes, nNodes))
    lastNodeId = np.cumsum(nPerLay)
    for i in range((len(lastNodeId) - 1)):
        if (i == 0):
            src = np.arange(0, lastNodeId[i])
        else:
            src = dest
        dest = np.arange((src[(- 1)] + 1), lastNodeId[(i + 1)])
        for s in src:
            adjMat[(s, dest)] = 1
    return adjMat
