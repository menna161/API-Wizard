from baconian.envs.gym_env import make
from baconian.core.core import EnvSpec
from baconian.test.tests.set_up.setup import BaseTestCase
from baconian.common.data_pre_processing import *
import numpy as np
from baconian.common.spaces import Box
from baconian.common.spaces import Box


def test_min_max(self):
    for env in (make('Pendulum-v0'), make('Acrobot-v1'), make('HalfCheetahBulletEnv-v0')):
        for sample_space in (env.observation_space, env.action_space):
            sample_fn = sample_space.sample
            dims = sample_space.flat_dim
            try:
                print('test {} with sample {} dims {}'.format(env, sample_fn, dims))
                min_max = BatchMinMaxScaler(dims=dims)
                data_list = []
                for i in range(100):
                    data_list.append(sample_fn())
                data = min_max.process(np.array(data_list))
                self.assertTrue(np.greater_equal(np.ones(dims), data).all())
                self.assertTrue(np.less_equal(np.zeros(dims), data).all())
                min_max = BatchMinMaxScaler(dims=dims, desired_range=((np.ones(dims) * (- 1.0)), (np.ones(dims) * 5.0)))
                data_list = []
                for i in range(100):
                    data_list.append(sample_fn())
                data = min_max.process(np.array(data_list))
                self.assertTrue(np.greater_equal((np.ones(dims) * 5.0), data).all())
                self.assertTrue(np.less_equal((np.ones(dims) * (- 1.0)), data).all())
                self.assertEqual(np.max(data), 5.0)
                self.assertEqual(np.min(data), (- 1.0))
                data = min_max.inverse_process(data)
                self.assertTrue(np.isclose(data, np.array(data_list)).all())
                data_list = []
                for i in range(100):
                    data_list.append(sample_fn())
                min_max = RunningMinMaxScaler(dims=dims, desired_range=((np.ones(dims) * (- 1.0)), (np.ones(dims) * 5.0)), init_data=np.array(data_list))
                data = min_max.process(np.array(data_list))
                self.assertTrue(np.greater_equal((np.ones(dims) * 5.0), data).all())
                self.assertTrue(np.less_equal((np.ones(dims) * (- 1.0)), data).all())
                self.assertEqual(np.max(data), 5.0)
                self.assertEqual(np.min(data), (- 1.0))
                data_list = []
                for i in range(100):
                    data_list.append(sample_fn())
                min_max = RunningMinMaxScaler(dims=dims, desired_range=((np.ones(dims) * (- 1.0)), (np.ones(dims) * 5.0)), init_min=np.min(np.array(data_list), axis=0), init_max=np.max(np.array(data_list), axis=0))
                data = min_max.process(np.array(data_list))
                self.assertTrue(np.greater_equal((np.ones(dims) * 5.0), data).all())
                self.assertTrue(np.less_equal((np.ones(dims) * (- 1.0)), data).all())
                self.assertEqual(np.max(data), 5.0)
                self.assertEqual(np.min(data), (- 1.0))
                pre_min = np.min(np.array(data_list), axis=0)
                pre_max = np.max(np.array(data_list), axis=0)
                data_list = (np.array(data_list) * 2.0)
                min_max.update_scaler(data_list)
                self.assertTrue(np.equal((pre_min * 2.0), min_max._min).all())
                self.assertTrue(np.equal((pre_max * 2.0), min_max._max).all())
            except ShapeNotCompatibleError as e:
                from baconian.common.spaces import Box
                if isinstance(sample_space, Box):
                    raise ValueError
                else:
                    pass
