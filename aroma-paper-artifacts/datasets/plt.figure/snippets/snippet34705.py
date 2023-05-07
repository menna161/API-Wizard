import time
import baselines.common.tf_util as U
import numpy as np
from baselines.ppo1.pposgd_simple import learn
from baselines.ppo1.mlp_policy import MlpPolicy
from senseact.envs.sim_double_pendulum.sim_double_pendulum import DoubleInvertedPendulumEnv
from senseact.utils import tf_set_seeds
from helper import create_callback
from multiprocessing import Process, Value, Manager
import matplotlib.pyplot as plt


def plot_returns(env, batch_size, shared_returns, plot_running):
    'Plots episodic returns\n\n    Args:\n        env: An instance of DoubleInvertedPendulumEnv\n        batch_size: An int representing timesteps_per_batch provided to the PPO learn function\n        shared_returns: A manager dictionary object containing `episodic returns` and `episodic lengths`\n        plot_running: A multiprocessing Value object containing 0/1.\n            1: Continue plotting, 0: Terminate plotting loop\n    '
    print('Started plotting routine')
    import matplotlib.pyplot as plt
    plt.ion()
    time.sleep(5.0)
    fig = plt.figure(figsize=(20, 6))
    ax = fig.add_subplot(111)
    (hl11,) = ax.plot([], [])
    fig.suptitle('Simulated Double Pendulum', fontsize=14)
    ax.set_title('Learning Curve')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Average Returns')
    count = 0
    old_size = len(shared_returns['episodic_returns'])
    returns = []
    while plot_running.value:
        if ((count % 20) == 0):
            if (len(shared_returns['episodic_returns']) > old_size):
                returns.append(np.mean(shared_returns['episodic_returns'][(- (len(shared_returns['episodic_returns']) - old_size)):]))
                old_size = len(shared_returns['episodic_returns'])
                hl11.set_ydata(returns)
                hl11.set_xdata((batch_size * np.arange(len(returns))))
                ax.set_ylim([np.min(returns), np.max(returns)])
                ax.set_xlim([0, int((len(returns) * batch_size))])
                fig.canvas.draw()
                fig.canvas.flush_events()
        time.sleep(0.01)
        fig.canvas.draw()
        fig.canvas.flush_events()
        count += 1
