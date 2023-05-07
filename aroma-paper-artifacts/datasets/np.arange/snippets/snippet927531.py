from mpi4py import MPI
import numpy as np
import json
import os
import subprocess
import sys
import config
from model_grid_fc import make_model, simulate
from es import CMAES, SimpleGA, OpenES, PEPG
import argparse
import time


def next_batch(self, batch_size):
    result = np.arange(self._seed, (self._seed + batch_size)).tolist()
    self._seed += batch_size
    return result
