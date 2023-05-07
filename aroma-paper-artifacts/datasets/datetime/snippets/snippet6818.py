import csv
import os
import subprocess
import torch
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
from torch.utils.tensorboard import SummaryWriter
from collections import defaultdict


def __init__(self, agent_name, env_name, sample_frame_interval=10000.0, sample_episode_interval=100.0, train_step_interval=100.0, exp_info='default_experiments'):
    try:
        os.mkdir('runs')
    except FileExistsError:
        pass
    self.env_name = env_name
    self._add_scalar_interval = {'sample_frames': sample_frame_interval, 'sample_episodes': sample_episode_interval, 'train_steps': train_step_interval}
    current_time = str(datetime.now())
    self.log_dir = os.path.join('runs', exp_info, env_name, ('%s %s %s' % (agent_name, COMMIT_HASH, current_time)))
    self.log_dir = self.log_dir.replace(' ', '_')
    os.makedirs(self.log_dir)
    self.sample_frames = 0
    self.train_steps = 0
    self.sample_episodes = 0
    self._name_frame_history = defaultdict((lambda : 0))
    super().__init__(log_dir=self.log_dir)
