import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random


def train_step2(model, state_transitions, targetModel, num_actions):
    cur_states = torch.stack([torch.Tensor(s.state) for s in state_transitions])
    next_states = torch.stack([torch.Tensor(s.next_state) for s in state_transitions])
    rewards = torch.stack([torch.Tensor([s.reward]) for s in state_transitions])
    actions = torch.stack([torch.Tensor(get_one_hot(action, num_actions)) for s in state_transitions])
    mask = torch.stack([(torch.Tensor([0]) if s.done else torch.Tensor([1])) for s in state_transitions])
    with torch.no_grad():
        qevals_next = targetModel(next_states)
        qevals_next = qevals_next.max(axis=1)[0]
    model.opt.zero_grad()
    qevals = model(cur_states)
    print('qevals_next', qevals_next)
    print('qeval*actions ', torch.sum((qevals * actions), axis=1))
    loss = ((rewards + ((0.98 * qevals_next) * mask[(:, 0)])) - torch.sum((qevals * actions), axis=1)).mean()
    loss.backward()
    model.opt.step()
    print('Loss ', loss)
    return loss
