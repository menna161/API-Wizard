import torch
import torch.nn as nn


def __init__(self, avrg_net_args, env_bldr, device):
    super().__init__()
    self.args = avrg_net_args
    self.env_bldr = env_bldr
    self.n_actions = self.env_bldr.N_ACTIONS
    MPM = avrg_net_args.mpm_args.get_mpm_cls()
    self._relu = nn.ReLU(inplace=False)
    self._mpm = MPM(env_bldr=env_bldr, device=device, mpm_args=self.args.mpm_args)
    self._final_layer = nn.Linear(in_features=self._mpm.output_units, out_features=self.args.n_units_final)
    self._out_layer = nn.Linear(in_features=self.args.n_units_final, out_features=self.n_actions)
    self.to(device)
