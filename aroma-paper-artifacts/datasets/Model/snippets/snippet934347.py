import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random
from PIL import Image
from agent_and_model import DQNAgent, sars, Model, ReplayBuffer
import plotly.graph_objects as go

if (__name__ == '__main__'):
    DEBUGER_ON = True
    NUM_GAMES = 50000
    INITIAL_RANDOM_STEPS = 5000
    MAX_EPISODE_STEPS = 4000
    LEARNING_RATE = 0.001
    TARGET_MODEL_UPDATE_INTERVAL = 50
    GAMMA_DISCOUNT_FACTOR = 0.991
    EPSILON_MIN = 0.02
    EPSILON_START = 0.3
    EPSLILON_COUNT = 500
    RANDOM_GAME_EVERY = 5
    TRAIN_EVERY_N_STEPS = 60
    TRAINING_SAMPLE_SIZE = 32
    TRAINING_ITTERATIONS = 1
    PRINT_EVERY = 1
    RENDER_ENV = True
    LOAD_MODEL = False
    SAVE_MODEL = True
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 5
    epsilon = EPSILON_START
    env = gym.make('Pong-v0')
    observation = env.reset()
    rb = ReplayBuffer(20000)
    agent = DQNAgent(Model(env.observation_space.shape, env.action_space.n, lr=LEARNING_RATE), Model(env.observation_space.shape, env.action_space.n, lr=LEARNING_RATE))
    frame1 = []
    frame2 = []
    frame3 = []
    frame1 = agent.process_frame(observation)
    frame2 = agent.process_frame(observation)
    frame3 = agent.process_frame(observation)
    observation = np.concatenate((frame1, frame2, frame3), axis=1)
    observation = observation.reshape((1, 3, 160, (140 * 3)))
    if LOAD_MODEL:
        agent.model.load_state_dict(torch.load((('' + MODEL_ID) + MODEL_FILE_NAME)))
        agent.model.eval()
    step_counter = 0
    avg_reward = []
    all_scores = []
    rolling_average = 0
    for game in range(NUM_GAMES):
        episode_sars = []
        score = 0.0
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            action = 0
            if ((step_counter < INITIAL_RANDOM_STEPS) or (random() < epsilon) or ((game % RANDOM_GAME_EVERY) == 0)):
                action = env.action_space.sample()
            else:
                action = agent.get_actions(observation).item()
            frame3 = frame2
            frame2 = frame1
            (frame1, reward, done, info) = env.step(action)
            score += reward
            frame1 = agent.process_frame(frame1)
            observation_next = np.concatenate((frame1, frame2, frame3), axis=1)
            observation_next = observation_next.reshape((1, 3, 160, (140 * 3)))
            _sars = sars(observation, action, reward, observation_next, done, 0.0)
            episode_sars.append(_sars)
            avg_reward.append([reward])
            if ((rb.index > INITIAL_RANDOM_STEPS) and ((step_counter % TRAIN_EVERY_N_STEPS) == 0)):
                for s in range(TRAINING_ITTERATIONS):
                    dick = rb.sample(TRAINING_SAMPLE_SIZE, step)
                    train_step2(agent.model, dick, agent.targetModel, env.action_space.n, GAMMA_DISCOUNT_FACTOR)
            observation = observation_next
            step_counter += 1
            if done:
                episode_sars = update_Qs(episode_sars, step_counter, step, len(episode_sars))
                for j in range(len(episode_sars)):
                    rb.insert(episode_sars[j])
                if (SAVE_MODEL and ((game % SAVE_MODEL_EVERY) == 0) and (game > 10)):
                    torch.save(agent.model, (('' + MODEL_ID) + MODEL_FILE_NAME))
                observation = env.reset()
                frame1 = agent.process_frame(observation)
                frame2 = agent.process_frame(observation)
                frame3 = agent.process_frame(observation)
                observation = np.concatenate((frame1, frame2, frame3), axis=1)
                observation = observation.reshape((1, 3, 160, (140 * 3)))
                break
        all_scores.append(score)
        rolling_average = ((score * 0.05) + ((1 - 0.05) * rolling_average))
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            plot_score(all_scores)
            print('episide ', game, 'game score', score, 'rolling score', rolling_average, 'episode_len', len(episode_sars), 'buffer', min(rb.index, rb.buffer_size), 'score', np.average(avg_reward), 'epsilon', epsilon)
        avg_reward = []
