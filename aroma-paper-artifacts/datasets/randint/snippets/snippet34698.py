import argparse
import time
import copy
import numpy as np
import baselines.common.tf_util as U
from baselines.trpo_mpi.trpo_mpi import learn
from baselines.ppo1.mlp_policy import MlpPolicy
from senseact.envs.dxl.dxl_tracker_env import DxlTracker1DEnv
from senseact.utils import tf_set_seeds, NormalizedEnv
from multiprocessing import Process, Value, Manager
from helper import create_callback
import matplotlib.pyplot as plt


def main(port, id, baud):
    rand_state = np.random.RandomState(1).get_state()
    np.random.set_state(rand_state)
    tf_set_seeds(np.random.randint(1, ((2 ** 31) - 1)))
    env = DxlTracker1DEnv(setup='dxl_tracker_default', dxl_dev_path=port, idn=id, baudrate=baud, obs_history=1, dt=0.04, gripper_dt=0.01, rllab_box=False, episode_length_step=None, episode_length_time=4, max_torque_mag=50, control_type='torque', target_type='position', reset_type='zero', reward_type='linear', use_ctypes_driver=True, random_state=rand_state)
    env = NormalizedEnv(env)
    env.start()
    sess = U.single_threaded_session()
    sess.__enter__()

    def policy_fn(name, ob_space, ac_space):
        return MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space, hid_size=32, num_hid_layers=2)
    plot_running = Value('i', 1)
    shared_returns = Manager().dict({'write_lock': False, 'episodic_returns': [], 'episodic_lengths': []})
    pp = Process(target=plot_dxl_tracker, args=(env, 2048, shared_returns, plot_running))
    pp.start()
    kindred_callback = create_callback(shared_returns)
    learn(env, policy_fn, max_timesteps=150000, timesteps_per_batch=2048, max_kl=0.05, cg_iters=10, cg_damping=0.1, vf_iters=5, vf_stepsize=0.001, gamma=0.995, lam=0.995, callback=kindred_callback)
    plot_running.value = 0
    time.sleep(2)
    pp.join()
    env.close()
