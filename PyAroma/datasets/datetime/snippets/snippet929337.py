from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import functools
import tensorflow as tf
from dreamer import tools
from dreamer.training import define_summaries
from dreamer.training import utility


def define_model(logdir, metrics, data, trainer, config):
    print('Build TensorFlow compute graph.')
    dependencies = []
    cleanups = []
    step = trainer.step
    global_step = trainer.global_step
    phase = trainer.phase
    timestamp = tf.py_func((lambda : datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')), [], tf.string)
    dependencies.append(metrics.set_tags(global_step=global_step, step=step, phase=phase, time=timestamp))
    try:
        cell = config.cell()
    except TypeError:
        cell = config.cell(action_size=data['action'].shape[(- 1)].value)
    kwargs = dict(create_scope_now_=True)
    encoder = tf.make_template('encoder', config.encoder, **kwargs)
    heads = tools.AttrDict(_unlocked=True)
    raw_dummy_features = cell.features_from_state(cell.zero_state(1, tf.float32))[(:, None)]
    for (key, head) in config.heads.items():
        name = 'head_{}'.format(key)
        kwargs = dict(create_scope_now_=True)
        if (key in data):
            kwargs['data_shape'] = data[key].shape[2:].as_list()
        if (key == 'action_target'):
            kwargs['data_shape'] = data['action'].shape[2:].as_list()
        if (key == 'cpc'):
            kwargs['data_shape'] = [cell.feature_size]
            dummy_features = encoder(data)[(:1, :1)]
        else:
            dummy_features = raw_dummy_features
        heads[key] = tf.make_template(name, head, **kwargs)
        heads[key](dummy_features)
    if ('value_target' in heads):
        dependencies.append(tools.track_network(trainer, config.batch_shape[0], '.*/head_value/.*', '.*/head_value_target/.*', config.value_target_period, config.value_target_update))
    if ('value_target_2' in heads):
        dependencies.append(tools.track_network(trainer, config.batch_shape[0], '.*/head_value/.*', '.*/head_value_target_2/.*', config.value_target_period, config.value_target_update))
    if ('action_target' in heads):
        dependencies.append(tools.track_network(trainer, config.batch_shape[0], '.*/head_action/.*', '.*/head_action_target/.*', config.action_target_period, config.action_target_update))
    embedded = encoder(data)
    with tf.control_dependencies(dependencies):
        embedded = tf.identity(embedded)
    graph = tools.AttrDict(locals())
    (prior, posterior) = tools.unroll.closed_loop(cell, embedded, data['action'], config.debug)
    objectives = utility.compute_objectives(posterior, prior, data, graph, config)
    (summaries, grad_norms) = utility.apply_optimizers(objectives, trainer, config)
    dependencies += summaries
    with tf.variable_scope('collection'):
        with tf.control_dependencies(dependencies):
            for (name, params) in config.train_collects.items():
                schedule = tools.schedule.binary(step, config.batch_shape[0], params.steps_after, params.steps_every, params.steps_until)
                (summary, _) = tf.cond(tf.logical_and(tf.equal(trainer.phase, 'train'), schedule), functools.partial(utility.simulate, metrics, config, params, graph, cleanups, gif_summary=False, name=name), (lambda : (tf.constant(''), tf.constant(0.0))), name=('should_collect_' + name))
                summaries.append(summary)
                dependencies.append(summary)
    graph = tools.AttrDict(locals())
    (summary, score) = tf.cond(trainer.log, (lambda : define_summaries.define_summaries(graph, config, cleanups)), (lambda : (tf.constant(''), tf.zeros((0,), tf.float32))), name='summaries')
    summaries = tf.summary.merge([summaries, summary])
    dependencies.append(utility.print_metrics({ob.name: ob.value for ob in objectives}, step, config.print_metrics_every, 2, 'objectives'))
    dependencies.append(utility.print_metrics(grad_norms, step, config.print_metrics_every, 2, 'grad_norms'))
    dependencies.append(tf.cond(trainer.log, metrics.flush, tf.no_op))
    with tf.control_dependencies(dependencies):
        score = tf.identity(score)
    return (score, summaries, cleanups)
