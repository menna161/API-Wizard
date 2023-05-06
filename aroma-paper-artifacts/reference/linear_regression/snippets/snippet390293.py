from baconian.test.tests.set_up.setup import TestWithAll
import numpy as np
from baconian.algo.dynamics.linear_dynamics_model import LinearDynamicsModel, LinearRegressionDynamicsModel
from baconian.common.data_pre_processing import RunningStandardScaler


def test_linear_regression_model(self):
    real_env = self.create_env('Pendulum-v0')
    real_env.init()
    x = real_env.observation_space.flat_dim
    u = real_env.action_space.flat_dim
    a = LinearRegressionDynamicsModel(env_spec=real_env.env_spec, state_input_scaler=RunningStandardScaler(dims=real_env.observation_space.flat_dim), action_input_scaler=RunningStandardScaler(dims=real_env.action_space.flat_dim), state_output_scaler=RunningStandardScaler(dims=real_env.observation_space.flat_dim))
    data = self.sample_transition(env=real_env, count=100)
    a.train(batch_data=data)
    predict = []
    for (state, action) in zip(data.state_set, data.action_set):
        predict.append(a.step(state=state, action=action))
    print(np.linalg.norm((np.array(predict) - data.new_state_set), ord=1))
    print(np.linalg.norm((np.array(predict) - data.new_state_set), ord=2))
