import torch.nn as nn


def __init__(self, env_bldr, adv_net_args, device):
    super().__init__()
    self._env_bldr = env_bldr
    self._args = adv_net_args
    self._n_actions = env_bldr.N_ACTIONS
    self._relu = nn.ReLU(inplace=False)
    MPM = adv_net_args.mpm_args.get_mpm_cls()
    self._mpm = MPM(env_bldr=env_bldr, device=device, mpm_args=adv_net_args.mpm_args)
    self._final_layer = nn.Linear(in_features=self._mpm.output_units, out_features=adv_net_args.n_units_final)
    self._adv = nn.Linear(in_features=adv_net_args.n_units_final, out_features=self._n_actions)
    self.to(device)
