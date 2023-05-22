import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random
from agent_and_model import sars, DQNAgent, ActorModel, CriticModel, ReplayBuffer
import plotly.graph_objects as go

if (__name__ == '__main__'):
    DEBUGER_ON = True
    NUM_GAMES = 80000
    MAX_EPISODE_STEPS = 400
    TARGET_MODEL_UPDATE_INTERVAL = 50
    EPSILON_MIN = 0.05
    EPSILON_START = 0.25
    EPSLILON_COUNT = 1000
    INITIAL_RANDOM_STEPS = 5000
    RANDOM_GAME_EVERY = 10
    NOISY_AGENT_GAME_EVERY = 3
    CRITIC_TRAINING_ITTERATIONS = 8
    TRAIN_CRITIC_EVERY_N_STEP = 15
    CRITIC_TRAINING_SAMPLE_SIZE = 1
    TRAIN_ACTOR_EVERY_N_STEP = 50
    TRAIN_ACTOR_EVERY_N_GAME = 1
    ACTOR_TRAINING_SAMPLE_SIZE = 1
    ACTOR_TRAINING_ITTERTIONS = 8
    LAST_EPISODE_TRAINING_SAMPLE_SIZE = 8
    PRINT_EVERY = 1
    RENDER_ENV = False
    LOAD_MODEL = False
    SAVE_MODEL = True
    MODEL_FILE_NAME = 'TDQN_RL_MODEL.trl'
    MODEL_ID = '01'
    SAVE_MODEL_EVERY = 10
    epsilon = EPSILON_START
    env = gym.make('LunarLanderContinuous-v2')
    observation = env.reset()
    rb = ReplayBuffer(400000)
    print('env action space ', env.action_space.shape)
    am = ActorModel(env.observation_space.shape, env.action_space.shape, lr=0.000101)
    cm = CriticModel(env.observation_space.shape, env.action_space.shape, lr=0.0001)
    agent = DQNAgent(am, cm)
    n_am = ActorModel(env.observation_space.shape, env.action_space.shape, lr=0.008)
    n_cm = CriticModel(env.observation_space.shape, env.action_space.shape, lr=0.01)
    noisy_agent = DQNAgent(n_am, n_cm)
    if LOAD_MODEL:
        agent.actor_model.load_state_dict(torch.load((('actor' + MODEL_ID) + MODEL_FILE_NAME)))
        agent.critic_model.load_state_dict(torch.load((('critic' + MODEL_ID) + MODEL_FILE_NAME)))
        agent.actor_model.eval()
        agent.critic_model.eval()
    step_counter = 0
    avg_reward = []
    action = []
    all_scores = []
    for game in range(NUM_GAMES):
        score = 0
        episode_sars = []
        if ((game % NOISY_AGENT_GAME_EVERY) == 0):
            print('adding param noise')
            noisy_agent.actor_model.load_state_dict(agent.actor_model.state_dict())
            with torch.no_grad():
                for param in noisy_agent.actor_model.parameters():
                    param.add_((torch.randn(param.size()).to(noisy_agent.actor_model.device) * 0.02))
        for step in range(MAX_EPISODE_STEPS):
            if RENDER_ENV:
                env.render()
            action = []
            if ((step_counter < INITIAL_RANDOM_STEPS) or (random() < epsilon) or ((game % RANDOM_GAME_EVERY) == 0)):
                action = env.action_space.sample()
            elif ((step_counter >= INITIAL_RANDOM_STEPS) and ((game % NOISY_AGENT_GAME_EVERY) == 0)):
                if ((step % 100) == 0):
                    print('noisy agent acting')
                action = noisy_agent.get_actions(observation).cpu().detach().numpy()
            else:
                action = agent.get_actions(observation).cpu().detach().numpy()
            (observation_next, reward, done, info) = env.step(action)
            if (step >= MAX_EPISODE_STEPS):
                done = True
            _sars = sars(observation, action, reward, observation_next, done, 0.0)
            episode_sars.append(_sars)
            avg_reward.append([reward])
            score += reward
            if ((rb.index > INITIAL_RANDOM_STEPS) and ((step_counter % TRAIN_CRITIC_EVERY_N_STEP) == 0)):
                for s in range(CRITIC_TRAINING_ITTERATIONS):
                    samples = rb.sample(CRITIC_TRAINING_SAMPLE_SIZE, step)
                    train_critic(agent.critic_model, samples, env.action_space.shape[0])
            if ((rb.index > INITIAL_RANDOM_STEPS) and ((step_counter % TRAIN_ACTOR_EVERY_N_STEP) == 0)):
                for s in range(ACTOR_TRAINING_ITTERTIONS):
                    samples = rb.sample(ACTOR_TRAINING_SAMPLE_SIZE, 0)
                    if ((rb.index > INITIAL_RANDOM_STEPS) and ((game % TRAIN_ACTOR_EVERY_N_GAME) == 0)):
                        train_actor(agent.actor_model, agent.critic_model, noisy_agent.actor_model, samples, ACTOR_TRAINING_SAMPLE_SIZE, env.action_space.shape[0])
            observation = observation_next
            step_counter += 1
            if done:
                episode_sars = update_Qs(episode_sars, step_counter, step, len(episode_sars))
                for j in range(len(episode_sars)):
                    rb.insert(episode_sars[j])
                if (SAVE_MODEL and ((game % SAVE_MODEL_EVERY) == 0) and (game > 50)):
                    torch.save(agent.actor_model, (('A2C_actor' + MODEL_ID) + MODEL_FILE_NAME))
                    torch.save(agent.critic_model, (('A2C_critic' + MODEL_ID) + MODEL_FILE_NAME))
                break
        observation = env.reset()
        for s in range(ACTOR_TRAINING_ITTERTIONS):
            samples = rb.sample(ACTOR_TRAINING_SAMPLE_SIZE, 0)
            if ((rb.index > INITIAL_RANDOM_STEPS) and ((game % TRAIN_ACTOR_EVERY_N_GAME) == 0)):
                train_actor(agent.actor_model, agent.critic_model, noisy_agent.actor_model, samples, ACTOR_TRAINING_SAMPLE_SIZE, env.action_space.shape[0])
        if ((rb.index > INITIAL_RANDOM_STEPS) and ((step_counter % TRAIN_CRITIC_EVERY_N_STEP) == 0)):
            for s in range(CRITIC_TRAINING_ITTERATIONS):
                samples = rb.sample(CRITIC_TRAINING_SAMPLE_SIZE, step)
                train_critic(agent.critic_model, samples, env.action_space.shape[0])
        epsilon = max(EPSILON_MIN, (epsilon - ((EPSILON_START - EPSILON_MIN) / EPSLILON_COUNT)))
        all_scores.append(score)
        if ((game % PRINT_EVERY) == 0):
            plot_score(all_scores)
            print('episide ', game, 'score', score, 'episode_len', len(episode_sars), 'buffer', min(rb.index, rb.buffer_size), 'score', np.average(avg_reward), 'epsilon', epsilon)
        avg_reward = []
