import torch.nn as nn


def __init__(self, env_bldr, q_args, device):
    super().__init__()
    self._env_bldr = env_bldr
    self._args = q_args
    self._n_actions = env_bldr.N_ACTIONS
    self._relu = nn.ReLU(inplace=False)
    MPM = q_args.mpm_args.get_mpm_cls()
    self._mpm = MPM(env_bldr=env_bldr, device=device, mpm_args=q_args.mpm_args)
    self._final_layer = nn.Linear(in_features=self._mpm.output_units, out_features=q_args.n_units_final)
    self._val = nn.Linear(in_features=q_args.n_units_final, out_features=self._n_actions)
    self.to(device)
