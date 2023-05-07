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
    MAX_EPISODE_STEPS = 1400
    TARGET_MODEL_UPDATE_INTERVAL = 50
    GAMMA_DISCOUNT_FACTOR = 0.995
    EPSILON_MIN = 0.05
    EPSILON_START = 0.5
    EPSLILON_COUNT = 3000
    INITIAL_RANDOM_STEPS = 2000
    RANDOM_GAME_EVERY = 20
    TRAIN_CRITIC_EVERY_N_STEP = 3
    CRITIC_TRAINING_SAMPLE_SIZE = 256
    TRAIN_ACTOR_EVERY_N_STEPS = (25 * 2)
    ACTOR_TRAINING_SAMPLE_SIZE = 4
    NUM_ACTOR_TRAINING_SAMPLES = 20
    TRAINING_ITTERATIONS = 1
    NUM_ACTOR_TRAINING_SAMPLES = 128
    PRINT_EVERY = 1
    RENDER_ENV = False
    LOAD_MODEL = False
    SAVE_MODEL = True
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 25
    epsilon = EPSILON_START
    env = gym.make('LunarLanderContinuous-v2')
    observation = env.reset()
    rb = ReplayBuffer(50000)
    print('env action space ', env.action_space.shape)
    am = ActorModel(env.observation_space.shape, env.action_space.shape, lr=0.00101)
    cm = CriticModel(env.observation_space.shape, env.action_space.shape, lr=0.001)
    agent = DQNAgent(am, cm)
    if LOAD_MODEL:
        agent.actor_model.load_state_dict(torch.load((('actor' + MODEL_ID) + MODEL_FILE_NAME)))
        agent.critic_model.load_state_dict(torch.load((('critic' + MODEL_ID) + MODEL_FILE_NAME)))
        agent.actor_model.eval()
        agent.critic_model.eval()
    step_counter = 0
    avg_reward = []
    action = []
    for game in range(NUM_GAMES):
        episode_sars = []
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            action = []
            if ((step_counter < INITIAL_RANDOM_STEPS) or (random() < epsilon) or ((game % RANDOM_GAME_EVERY) == 0)):
                action = env.action_space.sample()
            else:
                action = agent.get_actions(observation).cpu().detach().numpy()
            (observation_next, reward, done, info) = env.step(action)
            _sars = sars(observation, action, reward, observation_next, done, 0.0, np.concatenate((observation, action)), None)
            episode_sars.append(_sars)
            avg_reward.append([reward])
            if ((rb.index > INITIAL_RANDOM_STEPS) and ((step_counter % TRAIN_CRITIC_EVERY_N_STEP) == 0)):
                print('Training critic.')
                for s in range(TRAINING_ITTERATIONS):
                    samples = rb.sample(CRITIC_TRAINING_SAMPLE_SIZE, step)
                    train_critic(agent.critic_model, samples, env.action_space.shape[0], GAMMA_DISCOUNT_FACTOR)
            if ((rb.index > (INITIAL_RANDOM_STEPS * 2)) and ((step_counter % TRAIN_ACTOR_EVERY_N_STEPS) == 0)):
                samples = rb.sample(ACTOR_TRAINING_SAMPLE_SIZE, 0)
                print('Training actor')
                train_actor(agent.actor_model, agent.critic_model, samples, NUM_ACTOR_TRAINING_SAMPLES, env.action_space.shape[0])
            observation = observation_next
            step_counter += 1
            if done:
                if (SAVE_MODEL and ((game % SAVE_MODEL_EVERY) == 0) and (game > 50)):
                    torch.save(agent.actor_model, (('actor' + MODEL_ID) + MODEL_FILE_NAME))
                    torch.save(agent.critic_model, (('critic' + MODEL_ID) + MODEL_FILE_NAME))
                observation = env.reset()
                break
        episode_sars = update_Qs(episode_sars, step_counter, len(episode_sars), len(episode_sars), GAMMA_DISCOUNT_FACTOR)
        for j in range(len(episode_sars)):
            rb.insert(episode_sars[j])
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        if ((game % PRINT_EVERY) == 0):
            print('episide ', game, 'last score', reward, 'episode_len', len(episode_sars), 'buffer', len(rb.buffer), 'score', np.average(avg_reward), 'epsilon', epsilon)
        avg_reward = []
        observation = env.reset()
