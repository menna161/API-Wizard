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


def next_seed(self):
    result = np.random.randint(self.limit)
    return result
