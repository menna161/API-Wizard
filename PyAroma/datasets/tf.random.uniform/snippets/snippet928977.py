from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf
from tensorflow_probability import distributions as tfd
from dreamer.tools import nested


def step(self, agent_indices, observ):
    observ = self._config.preprocess_fn(observ)
    observ = nested.map((lambda x: x[(:, None)]), observ)
    embedded = self._config.encoder(observ)[(:, 0)]
    state = nested.map((lambda tensor: tf.gather(tensor, agent_indices)), self._state)
    prev_action = (self._prev_action + 0)
    with tf.control_dependencies([prev_action]):
        use_obs = tf.ones(tf.shape(agent_indices), tf.bool)[(:, None)]
        (_, state) = self._cell((embedded, prev_action, use_obs), state)
    action = self._config.planner(self._cell, self._config.objective, state, embedded.shape[1:].as_list(), prev_action.shape[1:].as_list())
    action = action[(:, 0)]
    if self._config.exploration:
        expl = self._config.exploration
        scale = tf.cast(expl.scale, tf.float32)[None]
        if expl.schedule:
            scale *= expl.schedule(self._step)
        if expl.factors:
            scale *= np.array(expl.factors)
        if (expl.type == 'additive_normal'):
            action = tfd.Normal(action, scale[(:, None)]).sample()
        elif (expl.type == 'epsilon_greedy'):
            random_action = tf.one_hot(tfd.Categorical((0 * action)).sample(), action.shape[(- 1)])
            switch = tf.cast(tf.less(tf.random.uniform((self._num_envs,)), scale), tf.float32)[(:, None)]
            action = ((switch * random_action) + ((1 - switch) * action))
        else:
            raise NotImplementedError(expl.type)
    action = tf.clip_by_value(action, (- 1), 1)
    remember_action = self._prev_action.assign(action)
    remember_state = nested.map((lambda var, val: tf.scatter_update(var, agent_indices, val)), self._state, state, flatten=True)
    with tf.control_dependencies((remember_state + (remember_action,))):
        return tf.identity(action)
