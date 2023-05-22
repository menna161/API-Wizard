import cma
import gin
import numpy as np
import algorithms.abc_algorithm
from misc.utility import MAX_INT


def _create_rpc_requests(self, evaluate):
    'Create gRPC requests.'
    if evaluate:
        n_repeat = 1
        num_roll_outs = self._n_eval_roll_outs
        params_list = [self._algorithm.get_current_parameters()]
    else:
        n_repeat = self._n_repeat
        params_list = self._algorithm.get_population()
        num_roll_outs = (len(params_list) * n_repeat)
    env_seed_list = self._rnd.randint(low=0, high=MAX_INT, size=num_roll_outs)
    requests = []
    for (i, env_seed) in enumerate(env_seed_list):
        ix = (0 if evaluate else (i // n_repeat))
        requests.append(self._communication_helper.create_cma_request(roll_out_index=i, env_seed=env_seed, parameters=params_list[ix], evaluate=evaluate))
    return requests
