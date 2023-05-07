import collections
import random
import os
import torch
from torch import nn
from torch.nn import functional as F
import gym
import numpy as np
from skimage.transform import resize
from estorch import ES, VirtualBatchNorm
from mpi4py import MPI

if (__name__ == '__main__'):
    device = torch.device('cpu')
    n_proc = 1
    env_name = 'Breakout-v0'
    frame_skip = 4
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    reference_batch = []
    n_actions = 0
    if (((rank == 0) and (os.getenv('MPI_PARENT') is not None)) or (n_proc == 1)):
        env = gym.make(env_name)
        for _ in range(5):
            observation = env.reset()
            frames = collections.deque(maxlen=frame_skip)
            frame_buffer = collections.deque(maxlen=2)
            frame_buffer.append(observation)
            y_channel = (observation @ np.array([0.299, 0.587, 0.114]))
            y_channel = resize(y_channel, (84, 84, 1))
            for _ in range(frame_skip):
                frames.append(y_channel.transpose(2, 0, 1))
            done = False
            total_reward = 0
            n_actions = env.action_space.n
            while (not done):
                frame = torch.from_numpy(np.concatenate(frames)).float().unsqueeze(0).to(device)
                reference_batch.append(frame)
                action = np.random.randint(0, n_actions)
                for _ in range(frame_skip):
                    (observation, reward, done, info) = env.step(action)
                    if done:
                        break
                    frame_buffer.append(observation)
                    observation = np.max(np.stack(frame_buffer), axis=0)
                    y_channel = (observation @ np.array([0.299, 0.587, 0.114]))
                    y_channel = resize(y_channel, (84, 84, 1))
                    frames.append(y_channel.transpose(2, 0, 1))
                    total_reward += reward
        reference_batch = random.sample(reference_batch, 128)
        reference_batch = torch.cat(reference_batch)
        comm.bcast(reference_batch, root=0)
        comm.bcast(n_actions, root=0)
    elif (rank != 0):
        reference_batch = comm.bcast(reference_batch, root=0)
        n_actions = comm.bcast(n_actions, root=0)
    es = ES(policy=Policy, agent=Agent, optimizer=torch.optim.Adam, population_size=100, sigma=0.02, device=device, policy_kwargs={'n_actions': n_actions, 'xref': reference_batch}, agent_kwargs={'env_name': env_name, 'frame_skip': frame_skip, 'device': device}, optimizer_kwargs={'lr': 0.01})
    es.train(n_steps=100, n_proc=n_proc)
    reward = agent.rollout(es.policy, render=True)
    print(f'Latest Policy Reward: {reward}')
    policy = Policy(n_actions, reference_batch).to(device)
    policy.load_state_dict(es.best_policy_dict)
    reward = agent.rollout(policy, render=True)
    print(f'Best Policy Reward: {reward}')
