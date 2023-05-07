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


def compute_value_loss(config, graph, states, features, reward):
    if (reward is None):
        reward = graph.heads.reward(features).mode()
    if config.value_maxent:
        reward -= compute_action_divergence(features, graph, config)
        reward -= compute_state_divergence(states, graph, config)
    if config.value_loss_pcont:
        pcont = tf.stop_gradient(graph.heads.pcont(features).mean())
    else:
        pcont = tf.ones_like(reward)
    pcont *= config.value_discount
    pred = graph.heads.value(features)
    if ('value_target' in graph.heads):
        value = graph.heads.value_target(features).mode()
    else:
        value = pred.mode()
    bootstrap = None
    if config.value_bootstrap:
        reward = reward[(:, :(- 1))]
        value = value[(:, :(- 1))]
        pcont = pcont[(:, :(- 1))]
        bootstrap = value[(:, (- 1))]
    return_ = control.lambda_return(reward, value, bootstrap, pcont, config.value_lambda, axis=1, stop_gradient=True)
    return_ = tf.concat([return_, tf.zeros_like(return_[(:, (- 1):)])], 1)
    loss = (- pred.log_prob(return_)[(:, :(- 1))])
    if config.value_pcont_weight:
        loss *= tf.stop_gradient(tf.cumprod(tf.concat([tf.ones_like(pcont[(:, :1)]), pcont[(:, :(- 1))]], 1), 1))
    return loss
