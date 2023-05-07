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


def batchMpiEval(pop):
    ' Sends population to workers for evaluation one batch at a time '
    global nWorker
    nSlave = (nWorker - 1)
    nJobs = len(pop)
    nBatch = math.ceil((nJobs / nSlave))
    seed = np.random.randint(1000)
    fitness = np.empty(nJobs, dtype=np.float64)
    i = 0
    for iBatch in range(nBatch):
        for iWork in range(nSlave):
            if (i < nJobs):
                wVec = pop[i].flatten()
                nData = np.shape(wVec)[0]
                comm.send(nData, dest=(iWork + 1), tag=1)
                comm.Send(wVec, dest=(iWork + 1), tag=2)
                comm.send(seed, dest=(iWork + 1), tag=3)
            else:
                nData = 0
                comm.send(nData, dest=(iWork + 1))
            i = (i + 1)
        i -= nSlave
        for iWork in range(1, (nSlave + 1)):
            if (i < nJobs):
                workResult = np.empty(1, dtype='d')
                comm.Recv(workResult, source=iWork)
                fitness[i] = workResult
            i += 1
    return fitness
