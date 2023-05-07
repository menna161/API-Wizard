import torch
import random
import numpy as np
import sys
from Env.EnvWrapper import EnvWrapper
from Policy.PPO.PPOPolicy import PPOAtariCNN, PPOSmallAtariCNN
from .ReplayBuffer import ReplayBuffer


def gather_samples(self, max_step_count=10000):
    state = self.wrapped_env.reset()
    step_count = 0
    done = False
    while (not done):
        if (np.random.random() < 0.9):
            action = self.categorical(self.student_network.get_action(state))
        else:
            action = np.random.randint(0, self.wrapped_env.action_n)
        target_policy = self.teacher_network.get_action(state, logit=True)
        target_value = self.teacher_network.get_value(state)
        self.replay_buffer.add((np.array(state), target_policy, target_value))
        (state, _, done) = self.wrapped_env.step(action)
        step_count += 1
        if (step_count > max_step_count):
            return
