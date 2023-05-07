import os
import sys
import time
import math
import argparse
import subprocess
import numpy as np
from mpi4py import MPI
from neat_src import *
from domain import *
import pickle


def batchMpiEval(pop, sameSeedForEachIndividual=True):
    'Sends population to workers for evaluation one batch at a time.\n\n  Args:\n    pop - [Ind] - list of individuals\n      .wMat - (np_array) - weight matrix of network\n              [N X N] \n      .aVec - (np_array) - activation function of each node\n              [N X 1]\n\n  Return:\n    reward  - (np_array) - fitness value of each individual\n              [N X 1]\n\n  Todo:\n    * Asynchronous evaluation instead of batches\n  '
    global nWorker, hyp
    nSlave = (nWorker - 1)
    nJobs = len(pop)
    nBatch = math.ceil((nJobs / nSlave))
    if (sameSeedForEachIndividual is False):
        seed = np.random.randint(1000, size=nJobs)
    else:
        seed = np.random.randint(1000)
    reward = np.empty(nJobs, dtype=np.float64)
    i = 0
    for iBatch in range(nBatch):
        for iWork in range(nSlave):
            if (i < nJobs):
                wVec = pop[i].wMat.flatten()
                n_wVec = np.shape(wVec)[0]
                aVec = pop[i].aVec.flatten()
                n_aVec = np.shape(aVec)[0]
                comm.send(n_wVec, dest=(iWork + 1), tag=1)
                comm.Send(wVec, dest=(iWork + 1), tag=2)
                comm.send(n_aVec, dest=(iWork + 1), tag=3)
                comm.Send(aVec, dest=(iWork + 1), tag=4)
                if (sameSeedForEachIndividual is False):
                    comm.send(seed.item(i), dest=(iWork + 1), tag=5)
                else:
                    comm.send(seed, dest=(iWork + 1), tag=5)
            else:
                n_wVec = 0
                comm.send(n_wVec, dest=(iWork + 1))
            i = (i + 1)
        i -= nSlave
        for iWork in range(1, (nSlave + 1)):
            if (i < nJobs):
                workResult = np.empty(1, dtype='d')
                comm.Recv(workResult, source=iWork)
                reward[i] = workResult
            i += 1
    return reward
