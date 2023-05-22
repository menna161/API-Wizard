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


def compute_objectives(posterior, prior, target, graph, config):
    raw_features = graph.cell.features_from_state(posterior)
    heads = graph.heads
    if config.imagination_horizon:
        imagination_start = posterior
        if config.imagination_skip_last:
            imagination_start = tools.nested.map((lambda x: x[(:, :(- config.imagination_skip_last))]), imagination_start)
        raw_states = imagine_forward(imagination_start, config.imagination_horizon, graph, config, graph.heads.action, stop_grad_post_action=False, stop_grad_pre_action=config.stop_grad_pre_action)
    else:
        raw_states = None
    objectives = []
    for (name, scale) in sorted(config.loss_scales.items(), key=(lambda x: x[0])):
        if (config.loss_scales[name] == 0.0):
            continue
        if ((name in config.heads) and (name not in config.gradient_heads)):
            features = tf.stop_gradient(raw_features)
            include = '.*/head_{}/.*'.format(name)
            exclude = None
        else:
            features = raw_features
            include = None
            exclude = None
        if (name == 'divergence'):
            loss = graph.cell.divergence_from_states(posterior, prior)
            if (config.free_nats is not None):
                loss = tf.maximum(0.0, (loss - float(config.free_nats)))
            objectives.append(Objective('divergence', loss, min, include, exclude))
        elif (name == 'cpc'):
            pred = heads.cpc(graph.embedded)
            objective = compute_cpc_loss(pred, features, config)
            objectives.append(Objective('cpc', objective, max, include, exclude))
        elif (name == 'overshooting'):
            shape = tools.shape(graph.data['action'])
            length = tf.tile(tf.constant(shape[1])[None], [shape[0]])
            (_, priors, posteriors, mask) = tools.overshooting(graph.cell, {}, graph.embedded, graph.data['action'], length, config.overshooting_distance, posterior)
            (posteriors, priors, mask) = tools.nested.map((lambda x: x[(:, :, 1:(- 1))]), (posteriors, priors, mask))
            if config.os_stop_posterior_grad:
                posteriors = tools.nested.map(tf.stop_gradient, posteriors)
            loss = graph.cell.divergence_from_states(posteriors, priors)
            if (config.free_nats is not None):
                loss = tf.maximum(0.0, (loss - float(config.free_nats)))
            objectives.append(Objective('overshooting', loss, min, include, exclude))
        elif (name == 'value'):
            if (config.value_source == 'dataset'):
                loss = compute_value_loss(config, graph, priors, features, target['reward'])
            elif (config.value_source == 'model'):
                if (('action_target' in graph.heads) or (not config.imagination_horizon)):
                    if ('action_target' in graph.heads):
                        policy = graph.heads.action_target
                    else:
                        policy = graph.heads.action
                    states = imagine_forward(posterior, config.value_model_horizon, graph, config, policy)
                else:
                    states = raw_states
                feat = graph.cell.features_from_state(states)
                loss = compute_value_loss(config, graph, states, feat, None)
            else:
                raise NotImplementedError(config.value_source)
            objectives.append(Objective('value', loss, min, include, exclude))
        elif (name == 'action'):
            if (config.action_source == 'model'):
                if (not config.imagination_horizon):
                    states = imagine_forward(posterior, config.action_model_horizon, graph, config, policy=graph.heads.action, stop_grad_post_action=False)
                else:
                    states = raw_states
                feat = graph.cell.features_from_state(states)
                objective = compute_action_values(config, graph, states, feat)
                objectives.append(Objective('action', objective, max, include, exclude))
            elif (config.action_source == 'dataset'):
                objective = heads.action(features).log_prob(target[name])
                objective -= compute_action_divergence(features, graph, config)
                objectives.append(Objective('action', objective, max, include, exclude))
            else:
                raise NotImplementedError(config.action_source)
        elif (name == 'reward'):
            reward_mask = tf.squeeze(target['reward_mask'], [(- 1)])
            logprob = (heads.reward(features).log_prob(target[name]) * reward_mask)
            objectives.append(Objective('reward', logprob, max, include, exclude))
        elif ((name == 'pcont') and config.pcont_label_weight):
            terminal = tf.cast(tf.less(target[name], 0.5), tf.float32)
            logprob = heads[name](features).log_prob(target[name])
            logprob *= (1 + (terminal * (config.pcont_label_weight - 1)))
            objectives.append(Objective(name, logprob, max, include, exclude))
        else:
            logprob = heads[name](features).log_prob(target[name])
            objectives.append(Objective(name, logprob, max, include, exclude))
    objectives = [o._replace(value=tf.reduce_mean(o.value)) for o in objectives]
    return objectives
