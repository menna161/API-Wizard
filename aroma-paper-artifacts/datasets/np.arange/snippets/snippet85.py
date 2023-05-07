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


@lru_cache(maxsize=1)
def _center_function(population_size):
    centers = np.arange(0, population_size)
    centers = (centers / (population_size - 1))
    centers -= 0.5
    return centers
