import time
import copy
import numpy as np
import baselines.common.tf_util as U
from multiprocessing import Process, Value, Manager
from baselines.trpo_mpi.trpo_mpi import learn
from baselines.ppo1.mlp_policy import MlpPolicy
from senseact.envs.ur.reacher_env import ReacherEnv
from senseact.utils import tf_set_seeds, NormalizedEnv
from helper import create_callback
import argparse
import matplotlib.pyplot as plt


def plot_ur5_reacher(env, batch_size, shared_returns, plot_running):
    'Helper process for visualize the tasks and episodic returns.\n\n    Args:\n        env: An instance of ReacherEnv\n        batch_size: An int representing timesteps_per_batch provided to the PPO learn function\n        shared_returns: A manager dictionary object containing `episodic returns` and `episodic lengths`\n        plot_running: A multiprocessing Value object containing 0/1.\n            1: Continue plotting, 0: Terminate plotting loop\n    '
    print('Started plotting routine')
    import matplotlib.pyplot as plt
    plt.ion()
    time.sleep(5.0)
    fig = plt.figure(figsize=(20, 6))
    ax1 = fig.add_subplot(131)
    (hl1,) = ax1.plot([], [], markersize=10, marker='o', color='r')
    (hl2,) = ax1.plot([], [], markersize=10, marker='o', color='b')
    ax1.set_xlabel('X', fontsize=14)
    h = ax1.set_ylabel('Y', fontsize=14)
    h.set_rotation(0)
    ax3 = fig.add_subplot(132)
    (hl3,) = ax3.plot([], [], markersize=10, marker='o', color='r')
    (hl4,) = ax3.plot([], [], markersize=10, marker='o', color='b')
    ax3.set_xlabel('Z', fontsize=14)
    h = ax3.set_ylabel('Y', fontsize=14)
    h.set_rotation(0)
    ax2 = fig.add_subplot(133)
    (hl11,) = ax2.plot([], [])
    count = 0
    old_size = len(shared_returns['episodic_returns'])
    while plot_running.value:
        plt.suptitle('Reward: {:.2f}'.format(env._reward_.value), x=0.375, fontsize=14)
        hl1.set_ydata([env._x_target_[1]])
        hl1.set_xdata([env._x_target_[2]])
        hl2.set_ydata([env._x_[1]])
        hl2.set_xdata([env._x_[2]])
        ax1.set_ylim([env._end_effector_low[1], env._end_effector_high[1]])
        ax1.set_xlim([env._end_effector_low[2], env._end_effector_high[2]])
        ax1.set_title('X-Y plane', fontsize=14)
        ax1.set_xlim(ax1.get_xlim()[::(- 1)])
        ax1.set_ylim(ax1.get_ylim()[::(- 1)])
        hl3.set_ydata([env._x_target_[1]])
        hl3.set_xdata([env._x_target_[0]])
        hl4.set_ydata([env._x_[1]])
        hl4.set_xdata([env._x_[0]])
        ax3.set_ylim([env._end_effector_low[1], env._end_effector_high[1]])
        ax3.set_xlim([env._end_effector_low[0], env._end_effector_high[0]])
        ax3.set_title('Y-Z plane', fontsize=14)
        ax3.set_xlim(ax3.get_xlim()[::(- 1)])
        ax3.set_ylim(ax3.get_ylim()[::(- 1)])
        copied_returns = copy.deepcopy(shared_returns)
        if ((not copied_returns['write_lock']) and (len(copied_returns['episodic_returns']) > old_size)):
            returns = np.array(copied_returns['episodic_returns'])
            old_size = len(copied_returns['episodic_returns'])
            window_size_steps = 5000
            x_tick = 1000
            if copied_returns['episodic_lengths']:
                ep_lens = np.array(copied_returns['episodic_lengths'])
            else:
                ep_lens = (batch_size * np.arange(len(returns)))
            cum_episode_lengths = np.cumsum(ep_lens)
            if (cum_episode_lengths[(- 1)] >= x_tick):
                steps_show = np.arange(x_tick, (cum_episode_lengths[(- 1)] + 1), x_tick)
                rets = []
                for i in range(len(steps_show)):
                    rets_in_window = returns[((cum_episode_lengths > max(0, ((x_tick * (i + 1)) - window_size_steps))) * (cum_episode_lengths < (x_tick * (i + 1))))]
                    if rets_in_window.any():
                        rets.append(np.mean(rets_in_window))
                hl11.set_xdata((np.arange(1, (len(rets) + 1)) * x_tick))
                ax2.set_xlim([x_tick, (len(rets) * x_tick)])
                hl11.set_ydata(rets)
                ax2.set_ylim([np.min(rets), (np.max(rets) + 50)])
        time.sleep(0.01)
        fig.canvas.draw()
        fig.canvas.flush_events()
        count += 1
