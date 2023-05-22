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
    MAX_EPISODE_STEPS = 1000
    TARGET_MODEL_UPDATE_INTERVAL = 50
    EPSILON_MIN = 0.05
    EPSILON_START = 0.5
    EPSLILON_COUNT = 6000
    RANDOM_GAME_EVERY = 20
    TRAIN_EVERY_N_STEPS = 25
    TRAINING_SAMPLE_SIZE = 256
    TRAINING_ITTERATIONS = 1
    PRINT_EVERY = 2
    RENDER_ENV = False
    LOAD_MODEL = False
    SAVE_MODEL = True
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 25
    epsilon = EPSILON_START
    env = gym.make('LunarLander-v2')
    observation = env.reset()
    rb = ReplayBuffer(30000)
    agent = DQNAgent(Model(env.observation_space.shape, env.action_space.n, lr=0.01), Model(env.observation_space.shape, env.action_space.n, lr=0.01))
    if LOAD_MODEL:
        agent.model.load_state_dict(torch.load((('' + MODEL_ID) + MODEL_FILE_NAME)))
        agent.model.eval()
    step_counter = 0
    avg_reward = []
    for game in range(NUM_GAMES):
        episode_sars = []
        if ((game % TARGET_MODEL_UPDATE_INTERVAL) == 0):
            print('game', game, ' updating target model')
            agent.update_target_model()
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            action = 0
            if ((step_counter < 2000) or (random() < epsilon) or ((game % RANDOM_GAME_EVERY) == 0)):
                action = env.action_space.sample()
            else:
                action = agent.get_actions(observation).item()
            (observation_next, reward, done, info) = env.step(action)
            _sars = sars(observation, action, reward, observation_next, done, 0.0)
            episode_sars.append(_sars)
            avg_reward.append([reward])
            if ((rb.index > 3000) and ((step_counter % TRAIN_EVERY_N_STEPS) == 0)):
                for s in range(TRAINING_ITTERATIONS):
                    dick = rb.sample(TRAINING_SAMPLE_SIZE, step)
                    train_step(agent.model, dick, agent.targetModel, env.action_space.n)
            observation = observation_next
            step_counter += 1
            if done:
                episode_sars = update_Qs(episode_sars, step_counter, step, len(episode_sars))
                for j in range(len(episode_sars)):
                    rb.insert(episode_sars[j])
                if (SAVE_MODEL and ((game % SAVE_MODEL_EVERY) == 0) and (game > 50)):
                    torch.save(agent.model, (('' + MODEL_ID) + MODEL_FILE_NAME))
                observation = env.reset()
                break
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            print('episide ', game, 'last score', reward, 'episode_len', len(episode_sars), 'buffer', len(rb.buffer), 'score', np.average(avg_reward), 'epsilon', epsilon)
        avg_reward = []
