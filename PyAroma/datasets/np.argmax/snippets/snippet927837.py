import os
import numpy as np
import copy
from .ann import exportNet


def gatherData(self, pop, species):
    fitness = [ind.fitness for ind in pop]
    peakfit = [ind.fitMax for ind in pop]
    nodes = np.asarray([np.shape(ind.node)[1] for ind in pop])
    conns = np.asarray([ind.nConn for ind in pop])
    if (len(self.x_scale) is 0):
        self.x_scale = np.append(self.x_scale, len(pop))
    else:
        self.x_scale = np.append(self.x_scale, (self.x_scale[(- 1)] + len(pop)))
    self.elite.append(pop[np.argmax(fitness)])
    if (len(self.best) is 0):
        self.best = copy.deepcopy(self.elite)
    elif (self.elite[(- 1)].fitness > self.best[(- 1)].fitness):
        self.best = np.append(self.best, copy.deepcopy(self.elite[(- 1)]))
        self.newBest = True
    else:
        self.best = np.append(self.best, copy.deepcopy(self.best[(- 1)]))
        self.newBest = False
    self.node_med = np.append(self.node_med, np.median(nodes))
    self.conn_med = np.append(self.conn_med, np.median(conns))
    self.fit_med = np.append(self.fit_med, np.median(fitness))
    self.fit_max = np.append(self.fit_max, self.elite[(- 1)].fitness)
    self.fit_top = np.append(self.fit_top, self.best[(- 1)].fitness)
    self.fit_peak = np.append(self.fit_peak, self.best[(- 1)].fitMax)
    if (len(self.objVals) == 0):
        self.objVals = np.c_[(fitness, peakfit, conns)]
    else:
        self.objVals = np.c_[(self.objVals, np.c_[(fitness, peakfit, conns)])]
