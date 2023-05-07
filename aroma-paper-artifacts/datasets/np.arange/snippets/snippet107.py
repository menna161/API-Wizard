import copy
import os
import sys
import subprocess
from typing import List
from functools import lru_cache
from enum import Enum
from scipy import spatial
from mpi4py import MPI
import numpy as np
import torch
import inspect


def _get_policy(self):
    total_novelty = []
    for (policy, _) in self.meta_population:
        (reward, bc) = self.agent.rollout(policy)
        novelty = self._calculate_novelty(bc, self._archive)
        total_novelty.append(novelty)
    total_novelty = np.array(total_novelty)
    meta_population_probability = (total_novelty / np.sum(total_novelty))
    self.idx = np.random.choice(np.arange(len(self.meta_population), dtype=np.int), p=meta_population_probability)
    (policy, optimizer) = self.meta_population[self.idx]
    return (policy, optimizer)
