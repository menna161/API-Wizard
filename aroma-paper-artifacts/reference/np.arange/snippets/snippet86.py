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


def _compute_ranks(rewards):
    rewards = np.array(rewards)
    ranks = np.empty(rewards.size, dtype=int)
    ranks[rewards.argsort()] = np.arange(rewards.size)
    return ranks
