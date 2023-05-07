import numpy as np
import math
import copy
import json
from domain import *
from utils import *
from .nsga_sort import nsga_sort
from ._variation import evolvePop, recombine
from ._speciate import Species, speciate, compatDist, assignSpecies, assignOffspring


def initPop(self):
    'Initialize population with a list of random individuals\n    '
    p = self.p
    nodeId = np.arange(0, ((p['ann_nInput'] + p['ann_nOutput']) + 1), 1)
    node = np.empty((3, len(nodeId)))
    node[(0, :)] = nodeId
    node[(1, 0)] = 4
    node[(1, 1:(p['ann_nInput'] + 1))] = 1
    node[(1, (p['ann_nInput'] + 1):((p['ann_nInput'] + p['ann_nOutput']) + 1))] = 2
    node[(2, :)] = p['ann_initAct']
    nConn = ((p['ann_nInput'] + 1) * p['ann_nOutput'])
    ins = np.arange(0, (p['ann_nInput'] + 1), 1)
    outs = ((p['ann_nInput'] + 1) + np.arange(0, p['ann_nOutput']))
    conn = np.empty((5, nConn))
    conn[(0, :)] = np.arange(0, nConn, 1)
    conn[(1, :)] = np.tile(ins, len(outs))
    conn[(2, :)] = np.repeat(outs, len(ins))
    conn[(3, :)] = np.nan
    conn[(4, :)] = 1
    pop = []
    for i in range(p['popSize']):
        newInd = Ind(conn, node)
        newInd.conn[(3, :)] = ((2 * (np.random.rand(1, nConn) - 0.5)) * p['ann_absWCap'])
        newInd.conn[(4, :)] = (np.random.rand(1, nConn) < p['prob_initEnable'])
        newInd.express()
        newInd.birth = 0
        pop.append(copy.deepcopy(newInd))
    innov = np.zeros([5, nConn])
    innov[(0:3, :)] = pop[0].conn[(0:3, :)]
    innov[(3, :)] = (- 1)
    self.pop = pop
    self.innov = innov
