import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random

if (__name__ == '__main__'):
    NUM_GAMES = 50000
    MAX_EPISODE_STEPS = 600
    TARGET_MODEL_UPDATE_INTERVAL = 50
    EPSILON_MIN = 0.01
    EPSILON_START = 0.3
    EPSLILON_COUNT = 2000
    RANDOM_GAME_EVERY = 20
    TRAIN_EVERY_N_STEPS = 15
    PRINT_EVERY = 10
    epsilon = EPSILON_START
    env = gym.make('CartPole-v1')
    observation = env.reset()
    m = Model(env.observation_space.shape, env.action_space.n, lr=0.01)
    rb = ReplayBuffer(3000)
    agent = DQNAgent(m, Model(env.observation_space.shape, env.action_space.n, lr=0.01))
    step_counter = 0
    avg_reward = []
    for game in range(NUM_GAMES):
        episode_sars = []
        for step in range(MAX_EPISODE_STEPS):
            env.render()
            action = 0
            if ((step_counter < 1000) or (random() < epsilon) or ((game % RANDOM_GAME_EVERY) == 0)):
                action = env.action_space.sample()
            else:
                action = agent.get_actions(observation).item()
            (observation_next, reward, done, info) = env.step(action)
            if done:
                reward = (- 100)
            _sars = sars(observation, action, reward, observation_next, done, 0.0)
            episode_sars.append(_sars)
            avg_reward.append([reward])
            if ((rb.index > 3000) and ((step_counter % TRAIN_EVERY_N_STEPS) == 0)):
                train_step(agent.model, rb.sample(1, step), agent.targetModel, env.action_space.n)
            observation = observation_next
            step_counter += 1
            if done:
                rb.episode_sars = update_Qs(episode_sars, step_counter, step, len(episode_sars))
                for j in range(len(episode_sars)):
                    rb.insert(episode_sars[j])
                observation = env.reset()
                break
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            print('episide ', game, 'score', np.average(avg_reward), 'epsilon', epsilon)
        avg_reward = []
