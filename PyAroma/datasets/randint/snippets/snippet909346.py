from global_utils import print_summary
from options import parse_options
from global_utils import set_global_seed, save_performance, plot_data
import time
from agent_env_params import design_agent_and_env
from multiprocessing import Process
import random
from environment import Environment
from agent import Agent
from global_utils import save_plot_figure


def worker(agent_params, env_params, FLAGS, i):
    seed = (int(time.time()) + random.randint(0, 100))
    set_global_seed(seed)
    FLAGS.seed = seed
    env = Environment(env_params, FLAGS)
    agent = Agent(FLAGS, env, agent_params)
    run_HAC(FLAGS, env, agent, plot_figure=False, num=i)
