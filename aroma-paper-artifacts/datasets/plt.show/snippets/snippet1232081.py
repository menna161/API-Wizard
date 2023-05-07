from time import time
from collections import deque
import random
import numpy as np
import argparse
import gym
import torch
from torch.utils.tensorboard import SummaryWriter
import hrl4in
from hrl4in.utils.logging import logger
from hrl4in.rl.ppo import PPO, Policy, RolloutStorage, MetaPolicy, AsyncRolloutStorage
from hrl4in.utils.utils import *
from hrl4in.utils.args import *
import gibson2
from gibson2.envs.parallel_env import ParallelNavEnvironment
from gibson2.envs.locomotor_env import NavigateEnv, NavigateRandomEnv, InteractiveNavigateEnv
from IPython import embed
import matplotlib.pyplot as plt


def plot_action_mask(plot_env, meta_actor_critic, hidden_size, device):
    meta_recurrent_hidden_states = torch.zeros(1, hidden_size, device=device)
    masks = torch.zeros(1, 1, device=device)
    base_heat_map = np.zeros((plot_env.height, plot_env.width))
    arm_heat_map = np.zeros((plot_env.height, plot_env.width))
    plot_env.reset()
    plot_env.agent_orientation = 3
    plot_env.target_pos = np.array([3, 5])
    for col in range(1, (plot_env.width - 1)):
        if (col == (plot_env.width // 2)):
            continue
        if (col > (plot_env.width // 2)):
            plot_env.door_state = plot_env.door_max_state
        for row in range(1, (plot_env.height - 1)):
            plot_env.agent_pos = np.array([row, col])
            observations = [plot_env.get_state()]
            batch = batch_obs(observations)
            for sensor in batch:
                batch[sensor] = batch[sensor].to(device)
            with torch.no_grad():
                (_, _, _, _, _, _, action_mask_probs) = meta_actor_critic.act(batch, meta_recurrent_hidden_states, masks)
            base_heat_map[(row, col)] = (action_mask_probs[0][0].item() + action_mask_probs[0][2].item())
            arm_heat_map[(row, col)] = (action_mask_probs[0][1].item() + action_mask_probs[0][2].item())
            print(row, col, action_mask_probs)
    print(arm_heat_map)
    plt.figure(0)
    plt.imshow(base_heat_map, cmap='hot', interpolation='nearest')
    plt.figure(1)
    plt.imshow(arm_heat_map, cmap='hot', interpolation='nearest')
    plt.show()
    assert False
