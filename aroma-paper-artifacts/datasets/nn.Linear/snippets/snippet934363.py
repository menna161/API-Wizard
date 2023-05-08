import argparse
import pickle
from collections import namedtuple
from itertools import count
import os, time
import numpy as np
import matplotlib.pyplot as plt
import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Normal, Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler


def __init__(self):
    super(Actor, self).__init__()
    self.fc1 = nn.Linear(num_state, 100)
    self.action_head = nn.Linear(100, num_action)
