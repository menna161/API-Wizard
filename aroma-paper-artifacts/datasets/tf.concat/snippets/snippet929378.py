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


def compute_action_values(config, graph, states, features):
    reward = graph.heads.reward(features).mode()
    reward -= compute_action_divergence(features, graph, config)
    reward -= compute_state_divergence(states, graph, config)
    if config.action_loss_pcont:
        pcont = graph.heads.pcont(features).mean()
        if config.action_pcont_stop_grad:
            pcont = tf.stop_gradient(pcont)
    else:
        pcont = tf.ones_like(reward)
    pcont *= config.action_discount
    if ('value' not in graph.heads):
        return control.discounted_return(reward, pcont, bootstrap=None, axis=1, stop_gradient=False)
    value = graph.heads.value(features).mode()
    bootstrap = None
    if config.action_bootstrap:
        reward = reward[(:, :(- 1))]
        value = value[(:, :(- 1))]
        pcont = pcont[(:, :(- 1))]
        bootstrap = value[(:, (- 1))]
    return_ = control.lambda_return(reward, value, bootstrap, pcont, config.action_lambda, axis=1, stop_gradient=False)
    if config.action_pcont_weight:
        return_ *= tf.stop_gradient(tf.cumprod(tf.concat([tf.ones_like(pcont[(:, :1)]), pcont[(:, :(- 1))]], 1), 1))
    return return_
