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


def main(ip):
    rand_state = np.random.RandomState(1).get_state()
    np.random.set_state(rand_state)
    tf_set_seeds(np.random.randint(1, ((2 ** 31) - 1)))
    env = ReacherEnv(setup='UR5_default', host=ip, dof=2, control_type='velocity', target_type='position', reset_type='zero', reward_type='precision', derivative_type='none', deriv_action_max=5, first_deriv_max=2, accel_max=1.4, speed_max=0.3, speedj_a=1.4, episode_length_time=4.0, episode_length_step=None, actuation_sync_period=1, dt=0.04, run_mode='multiprocess', rllab_box=False, movej_t=2.0, delay=0.0, random_state=rand_state)
    env = NormalizedEnv(env)
    env.start()
    sess = U.single_threaded_session()
    sess.__enter__()

    def policy_fn(name, ob_space, ac_space):
        return MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space, hid_size=32, num_hid_layers=2)
    plot_running = Value('i', 1)
    shared_returns = Manager().dict({'write_lock': False, 'episodic_returns': [], 'episodic_lengths': []})
    pp = Process(target=plot_ur5_reacher, args=(env, 2048, shared_returns, plot_running))
    pp.start()
    kindred_callback = create_callback(shared_returns)
    learn(env, policy_fn, max_timesteps=150000, timesteps_per_batch=2048, max_kl=0.05, cg_iters=10, cg_damping=0.1, vf_iters=5, vf_stepsize=0.001, gamma=0.995, lam=0.995, callback=kindred_callback)
    plot_running.value = 0
    time.sleep(2)
    pp.join()
    env.close()
