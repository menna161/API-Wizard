import numpy as np
import torch
from PokerRL.rl import rl_util
from PokerRL.rl.neural.DuelingQNet import DuelingQNet
from PokerRL.rl.neural.NetWrapperBase import NetWrapperArgsBase as _NetWrapperArgsBase
from PokerRL.rl.neural.NetWrapperBase import NetWrapperBase as _NetWrapperBase


def select_br_a(self, pub_obses, range_idxs, legal_actions_lists, explore=False):
    if (explore and (np.random.random() < self._eps)):
        return np.array([legal_actions[np.random.randint(len(legal_actions))] for legal_actions in legal_actions_lists])
    with torch.no_grad():
        self.eval()
        range_idxs = torch.tensor(range_idxs, dtype=torch.long, device=self.device)
        q = self._net(pub_obses=pub_obses, range_idxs=range_idxs, legal_action_masks=rl_util.batch_get_legal_action_mask_torch(n_actions=self._env_bldr.N_ACTIONS, legal_actions_lists=legal_actions_lists, device=self.device, dtype=torch.float32)).cpu().numpy()
        for b in range(q.shape[0]):
            illegal_actions = [i for i in self._n_actions_arranged if (i not in legal_actions_lists[b])]
            if (len(illegal_actions) > 0):
                illegal_actions = np.array(illegal_actions)
                q[(b, illegal_actions)] = (- 1e+20)
        return np.argmax(q, axis=1)
