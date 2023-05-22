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


def evaluate_batch(model_params, max_len=(- 1)):
    solutions = []
    for i in range(es.popsize):
        solutions.append(np.copy(model_params))
    seeds = np.arange(es.popsize)
    packet_list = encode_solution_packets(seeds, solutions, train_mode=0, max_len=max_len)
    send_packets_to_slaves(packet_list)
    reward_list_total = receive_packets_from_slaves()
    reward_list = reward_list_total[(:, 0)]
    return np.mean(reward_list)
