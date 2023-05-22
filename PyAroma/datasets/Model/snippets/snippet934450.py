import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random
import ipdb

if (__name__ == '__main__'):
    DEBUGER_ON = False
    NUM_GAMES = 100
    MAX_EPISODE_STEPS = 1000
    TARGET_MODEL_UPDATE_INTERVAL = 50
    EPSILON_MIN = 0.05
    EPSILON_START = 0.5
    EPSLILON_COUNT = 6000
    RANDOM_GAME_EVERY = 20
    TRAIN_EVERY_N_STEPS = 300
    TRAINING_SAMPLE_SIZE = 512
    TRAINING_ITTERATIONS = 1
    PRINT_EVERY = 1
    RENDER_ENV = True
    LOAD_MODEL = True
    SAVE_MODEL = False
    TRAINING_ON = False
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 25
    epsilon = EPSILON_START
    env = gym.make('LunarLanderContinuous-v2')
    observation = env.reset()
    rb = ReplayBuffer(30000)
    am = ActorModel(env.observation_space.shape, env.action_space.shape, lr=0.01)
    cm = CriticModel(env.observation_space.shape, env.action_space.shape, lr=0.01)
    agent = DQNAgent(am, cm)
    if LOAD_MODEL:
        print('Loading Model ', (('' + MODEL_ID) + MODEL_FILE_NAME))
        agent.actor_model = torch.load((('actor' + MODEL_ID) + MODEL_FILE_NAME))
        agent.actor_model.eval()
    step_counter = 0
    avg_reward = []
    for game in range(NUM_GAMES):
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            action = agent.get_actions(observation).cpu().detach().numpy()
            (observation, reward, done, info) = env.step(action)
            if done:
                break
        observation = env.reset()
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            print('episide ', game, 'last score', reward, 'episode_len', 'score', np.average(avg_reward))
        avg_reward = []
