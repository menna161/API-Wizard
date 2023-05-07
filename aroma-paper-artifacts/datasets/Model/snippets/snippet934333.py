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
    DEBUGER_ON = True
    NUM_GAMES = 50000
    MAX_EPISODE_STEPS = 1490
    TARGET_MODEL_UPDATE_INTERVAL = 50
    EPSILON_MIN = 0.05
    EPSILON_START = 0.5
    EPSLILON_COUNT = 6000
    RANDOM_GAME_EVERY = 20
    TRAIN_EVERY_N_STEPS = 25
    TRAINING_SAMPLE_SIZE = 256
    TRAINING_ITTERATIONS = 1
    PRINT_EVERY = 1
    RENDER_ENV = True
    LOAD_MODEL = True
    SAVE_MODEL = False
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 25
    epsilon = EPSILON_START
    env = gym.make('LunarLander-v2')
    observation = env.reset()
    agent = DQNAgent(Model(env.observation_space.shape, env.action_space.n, lr=0.0001), Model(env.observation_space.shape, env.action_space.n, lr=0.0001))
    if LOAD_MODEL:
        print('Loading Model ', (('' + MODEL_ID) + MODEL_FILE_NAME))
        agent.model = torch.load((('' + MODEL_ID) + MODEL_FILE_NAME))
        agent.model.eval()
    step_counter = 0
    avg_reward = []
    last_step_count = 0
    for game in range(NUM_GAMES):
        score = 0
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            action = 0
            action = agent.get_actions(observation).item()
            (observation_next, reward, done, info) = env.step(action)
            score += reward
            observation = observation_next
            step_counter += 1
            last_step_count = step
            if done:
                observation = env.reset()
                break
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            print('episide ', game, 'last score', reward, 'game score ', score, 'episode_len', last_step_count, 'epsilon', epsilon)
        avg_reward = []
