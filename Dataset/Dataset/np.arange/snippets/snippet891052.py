import numpy as np
import torch
from PokerRL.rl import rl_util
from PokerRL.rl.neural.DuelingQNet import DuelingQNet
from PokerRL.rl.neural.NetWrapperBase import NetWrapperArgsBase as _NetWrapperArgsBase
from PokerRL.rl.neural.NetWrapperBase import NetWrapperBase as _NetWrapperBase


def __init__(self, env_bldr, ddqn_args, owner):
    super().__init__(net=DuelingQNet(env_bldr=env_bldr, q_args=ddqn_args.q_args, device=ddqn_args.device_training), env_bldr=env_bldr, args=ddqn_args, owner=owner, device=ddqn_args.device_training)
    self._eps = None
    self._target_net = DuelingQNet(env_bldr=env_bldr, q_args=ddqn_args.q_args, device=ddqn_args.device_training)
    self._target_net.eval()
    self.update_target_net()
    self._batch_arranged = torch.arange(ddqn_args.batch_size, dtype=torch.long, device=self.device)
    self._minus_e20 = torch.full((ddqn_args.batch_size, self._env_bldr.N_ACTIONS), fill_value=(- 1e+21), device=self.device, dtype=torch.float32, requires_grad=False)
    self._n_actions_arranged = np.arange(self._env_bldr.N_ACTIONS, dtype=np.int32).tolist()
