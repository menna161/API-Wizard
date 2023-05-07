import matplotlib.pylab as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def plot_sample_trajectory(env, policies, max_episode_length, state_names):
    'Plot sample trajectories from policies.\n    \n    Parameters\n    ----------\n        policies: A dictionary mapping policy names to policies.\n        max_episode_length: Max number of steps in the trajectory.\n    '
    (fig, axes) = plt.subplots(5, 2, sharex=True, figsize=[12, 12])
    axes = axes.flatten()
    for (name, policy) in policies.items():
        trajectory = sample_trajectory(env, policy, max_episode_length)
        obs = trajectory['observation']
        for i in range(len(state_names)):
            y = np.log(obs[(:, i)])
            axes[i].plot(y, label=name)
            axes[i].set_ylabel(('log ' + state_names[i]))
            (ymin, ymax) = axes[i].get_ylim()
            axes[i].set_ylim(np.minimum(ymin, y.min()), np.maximum(ymax, y.max()))
        action = np.array(trajectory['action'])
        epsilon_1 = (np.logical_or((action == 2), (action == 3)).astype(float) * 0.7)
        epsilon_2 = (np.logical_or((action == 1), (action == 3)).astype(float) * 0.3)
        axes[(- 3)].plot(epsilon_1, label=name)
        axes[(- 3)].set_ylabel('Treatment epsilon_1')
        axes[(- 3)].set_ylim((- 0.1), 1.0)
        axes[(- 2)].plot(epsilon_2, label=name)
        axes[(- 2)].set_ylabel('Treatment epsilon_2')
        axes[(- 2)].set_ylim((- 0.1), 1.0)
        reward = trajectory['reward']
        axes[(- 1)].plot(reward, label=name)
        axes[(- 1)].set_ylabel('reward')
        axes[(- 1)].ticklabel_format(scilimits=((- 2), 2))
        (ymin, ymax) = axes[(- 1)].get_ylim()
        axes[(- 1)].set_ylim(np.minimum(ymin, reward.min()), np.maximum(ymax, reward.max()))
        print(f'Total reward for {name}: {np.sum(reward):.2f}')
    for ax in axes:
        ax.legend()
        ax.set_xlabel('time (days)')
    plt.show()
