from baconian.common.data_pre_processing import DataScaler
from baconian.core.core import EnvSpec
from baconian.algo.dynamics.dynamics_model import GlobalDynamicsModel, TrainableDyanmicsModel
from baconian.core.parameters import Parameters
import numpy as np
from copy import deepcopy
from sklearn.linear_model import LinearRegression
from baconian.common.sampler.sample_data import TransitionData


def __init__(self, env_spec: EnvSpec, init_state=None, name='dynamics_model', state_input_scaler: DataScaler=None, action_input_scaler: DataScaler=None, state_output_scaler: DataScaler=None):
    super().__init__(env_spec=env_spec, init_state=init_state, name=name, state_input_scaler=state_input_scaler, action_input_scaler=action_input_scaler, state_output_scaler=state_output_scaler)
    self._linear_model = LinearRegression(fit_intercept=True, normalize=False)
