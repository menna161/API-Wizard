from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import datetime
import functools
import os
import re
import numpy as np
import ruamel.yaml as yaml
import tensorflow as tf
from dreamer import control
from dreamer import tools
from dreamer.training import trainer as trainer_


def collect_initial_episodes(metrics, config):
    items = config.random_collects.items()
    items = sorted(items, key=(lambda x: x[0]))
    for (name, params) in items:
        metrics.set_tags(global_step=0, step=0, phase=name.split('-')[0], time=datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S'))
        tf.gfile.MakeDirs(params.save_episode_dir)
        filenames = tf.gfile.Glob(os.path.join(params.save_episode_dir, '*.npz'))
        num_episodes = len(filenames)
        num_steps = sum([int(re.search('-([0-9]+)\\.npz', f).group(1)) for f in filenames])
        remaining_episodes = (params.num_episodes - num_episodes)
        remaining_steps = (params.num_steps - num_steps)
        if ((remaining_episodes <= 0) and (remaining_steps <= 0)):
            continue
        if params.give_rewards:
            env_ctor = params.task.env_ctor
            word = 'with'
        else:
            env_ctor = functools.partial((lambda ctor: control.wrappers.NoRewardHint(ctor())), params.task.env_ctor)
            word = 'without'
        message = 'Collecting initial {} episodes or {} steps ({}) {} rewards.'
        print(message.format(remaining_episodes, remaining_steps, name, word))
        episodes = control.random_episodes(env_ctor, remaining_episodes, remaining_steps, params.save_episode_dir, config.isolate_envs)
        scores = [episode['reward'].sum() for episode in episodes]
        lengths = [len(episode['reward']) for episode in episodes]
        metrics.add_scalars((name + '/return'), scores)
        metrics.add_scalars((name + '/length'), lengths)
    metrics.flush()
