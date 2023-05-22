from mpi4py import MPI
import numpy as np
import json
import os
import subprocess
import sys
import config
from model import make_model, simulate
from es import CMAES, SimpleGA, OpenES, PEPG
import argparse
import time


def next_batch(self, batch_size):
    result = np.random.randint(self.limit, size=batch_size).tolist()
    return result
