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


def main():
    rand_state = np.random.RandomState(1).get_state()
    np.random.set_state(rand_state)
    tf_set_seeds(np.random.randint(1, ((2 ** 31) - 1)))
    env = DoubleInvertedPendulumEnv(agent_dt=0.005, sensor_dt=[0.01, 0.0033333], is_render=False, random_state=rand_state)
    env.start()
    sess = U.single_threaded_session()
    sess.__enter__()

    def policy_fn(name, ob_space, ac_space):
        return MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space, hid_size=64, num_hid_layers=2)
    plot_running = Value('i', 1)
    shared_returns = Manager().dict({'write_lock': False, 'episodic_returns': [], 'episodic_lengths': []})
    pp = Process(target=plot_returns, args=(env, 2048, shared_returns, plot_running))
    pp.start()
    kindred_callback = create_callback(shared_returns)
    learn(env, policy_fn, max_timesteps=1000000.0, timesteps_per_actorbatch=2048, clip_param=0.2, entcoeff=0.0, optim_epochs=10, optim_stepsize=0.0001, optim_batchsize=64, gamma=0.995, lam=0.995, schedule='linear', callback=kindred_callback)
    plot_running.value = 0
    time.sleep(2)
    pp.join()
    env.close()
