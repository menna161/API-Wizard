import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random
from agent_and_model import sars, DQNAgent, CriticModel, ActorModel, ReplayBuffer

if (__name__ == '__main__'):
    DEBUGER_ON = True
    NUM_GAMES = 100
    MAX_EPISODE_STEPS = 10000
    TARGET_MODEL_UPDATE_INTERVAL = 50
    EPSILON_MIN = 0.05
    EPSILON_START = 0.5
    EPSLILON_COUNT = 6000
    INITIAL_RANDOM_STEPS = 5000
    RANDOM_GAME_EVERY = 20
    TRAIN_CRITIC_EVERY_N_STEP = 300
    CRITIC_TRAINING_SAMPLE_SIZE = 256
    TRAIN_ACTOR_EVERY_N_GAME = 1
    ACTOR_TRAINING_SAMPLE_SIZE = 8
    NUM_ACTOR_TRAINING_SAMPLES = 40
    TRAINING_ITTERATIONS = 1
    NUM_ACTOR_TRAINING_SAMPLES = 128
    PRINT_EVERY = 1
    RENDER_ENV = True
    LOAD_MODEL = True
    SAVE_MODEL = False
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 25
    epsilon = EPSILON_START
    env = gym.make('LunarLanderContinuous-v2')
    observation = env.reset()
    print('env action space ', env.action_space.shape)
    am = ActorModel(env.observation_space.shape, env.action_space.shape, lr=0.008)
    cm = CriticModel(env.observation_space.shape, env.action_space.shape, lr=0.01)
    agent = DQNAgent(am, cm)
    if LOAD_MODEL:
        agent.actor_model = torch.load((('A2C_actor' + MODEL_ID) + MODEL_FILE_NAME))
        agent.critic_model = torch.load((('A2C_critic' + MODEL_ID) + MODEL_FILE_NAME))
        agent.actor_model.eval()
        agent.critic_model.eval()
    step_counter = 0
    last_step_count = 0
    action = []
    for game in range(NUM_GAMES):
        episode_sars = []
        score = 0
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            if (random() < (- 0.1)):
                action = env.action_space.sample()
            else:
                action = agent.get_actions(observation).cpu().detach().numpy()
            (observation_next, reward, done, info) = env.step(action)
            score += reward
            observation = observation_next
            step_counter += 1
            last_step_count = step
            if done:
                break
        observation = env.reset()
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            print('episide ', game, 'last score', reward, 'game score ', score, 'episode_len', last_step_count, 'epsilon', epsilon)
        avg_reward = []
