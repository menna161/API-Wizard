import matplotlib.pylab as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def run_training_loop(env, n_iter=200, max_episode_length=100, batch_size=512, learning_rate=0.01):
    'Trains a neural network policy using policy gradients.\n\n    Parameters\n    ----------\n    n_iter: number of training iterations\n    max_episode_length: episode length, up to 400\n    batch_size: number of steps used in each iteration\n    learning_rate: learning rate for the Adam optimizer\n\n    Returns\n    -------\n    A Policy instance, the trained policy.\n    '
    total_timesteps = 0
    agent = PolicyGradientAgent(env=env, learning_rate=learning_rate)
    avg_rewards = np.zeros(n_iter)
    avg_episode_lengths = np.zeros(n_iter)
    loss = np.zeros(n_iter)
    for itr in range(n_iter):
        if ((itr % 10) == 0):
            print(f'*****Iteration {itr}*****')
        (trajectories, timesteps_this_itr) = sample_trajectories_by_batch_size(env, agent.actor, batch_size, max_episode_length)
        total_timesteps += timesteps_this_itr
        avg_rewards[itr] = np.mean([get_trajectory_total_reward(tau) for tau in trajectories])
        avg_episode_lengths[itr] = np.mean([get_trajectory_len(tau) for tau in trajectories])
        loss[itr] = agent.train(trajectories).item()
        agent.actor.epsilon = np.maximum(0.05, (agent.actor.epsilon * 0.97))
    (fig, (ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, figsize=[9, 9])
    ax1.plot(avg_rewards)
    ax1.set_xlabel('number of iterations')
    ax1.set_ylabel('average total reward')
    ax1.set_ylim(avg_rewards.min(), avg_rewards.max())
    ax2.plot(loss)
    ax2.set_xlabel('number of iterations')
    ax2.set_ylabel('training loss')
    ax2.set_ylim(loss.min(), loss.max())
    ax3.plot(avg_episode_lengths)
    ax3.set_xlabel('number of iterations')
    ax3.set_ylabel('average episode length')
    ax3.set_ylim(avg_episode_lengths.min(), avg_episode_lengths.max())
    plt.show()
    agent.actor.epsilon = 0.0
    return agent.actor
