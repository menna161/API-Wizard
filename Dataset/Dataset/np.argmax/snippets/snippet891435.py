import numpy as np
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerEnvStateDictEnums import EnvDictIdxs
from PokerRL.game._.tree._.nodes import PlayerActionNode


def compute_cf_values_heads_up(self, node):
    '\n        The functionality is extremely simplified compared to n-agent evaluations and made for HU Leduc only!\n        Furthermore, this BR implementation is *VERY* inefficient and not suitable for anything much bigger than Leduc.\n        '
    assert (self._tree.n_seats == 2)
    if node.is_terminal:
        assert (node.strategy is None)
    else:
        assert (node.strategy.shape == (self._env_bldr.rules.RANGE_SIZE, len(node.children)))
    if node.is_terminal:
        '\n            equity: -1*reach=always lose. 1*reach=always win. 0=50%/50%\n            '
        assert isinstance(node, PlayerActionNode)
        if (node.action == Poker.FOLD):
            if (node.env_state[EnvDictIdxs.current_round] == Poker.FLOP):
                equity = self._get_fold_eq_final_street(node=node)
            else:
                equity = self._get_fold_eq_preflop(node=node)
        elif (node.env_state[EnvDictIdxs.current_round] == Poker.FLOP):
            equity = self._get_call_eq_final_street(reach_probs=node.reach_probs, board_2d=node.env_state[EnvDictIdxs.board_2d])
        else:
            equity = self._get_call_eq_preflop(node=node)
        for c in self._env_bldr.lut_holder.get_1d_cards(node.env_state[EnvDictIdxs.board_2d]):
            if (c != Poker.CARD_NOT_DEALT_TOKEN_1D):
                equity[(:, c)] = 0.0
        node.ev = ((equity * node.env_state[EnvDictIdxs.main_pot]) / 2)
        node.ev_br = np.copy(node.ev)
    else:
        N_ACTIONS = len(node.children)
        ev_all_actions = np.zeros(shape=(N_ACTIONS, self._tree.n_seats, self._env_bldr.rules.RANGE_SIZE), dtype=np.float32)
        ev_br_all_actions = np.zeros(shape=(N_ACTIONS, self._tree.n_seats, self._env_bldr.rules.RANGE_SIZE), dtype=np.float32)
        for (i, child) in enumerate(node.children):
            self.compute_cf_values_heads_up(node=child)
            ev_all_actions[i] = child.ev
            ev_br_all_actions[i] = child.ev_br
        if (node.p_id_acting_next == self._tree.CHANCE_ID):
            node.ev = np.sum(ev_all_actions, axis=0)
            node.ev_br = np.sum(ev_br_all_actions, axis=0)
        else:
            node.ev = np.zeros(shape=(self._tree.n_seats, self._env_bldr.rules.RANGE_SIZE), dtype=np.float32)
            node.ev_br = np.zeros(shape=(self._tree.n_seats, self._env_bldr.rules.RANGE_SIZE), dtype=np.float32)
            plyr = node.p_id_acting_next
            opp = (1 - node.p_id_acting_next)
            node.ev[plyr] = np.sum((node.strategy.T * ev_all_actions[(:, plyr)]), axis=0)
            node.ev[opp] = np.sum(ev_all_actions[(:, opp)], axis=0)
            node.ev_br[opp] = np.sum(ev_br_all_actions[(:, opp)], axis=0)
            node.ev_br[plyr] = np.max(ev_br_all_actions[(:, plyr)], axis=0)
            node.br_a_idx_in_child_arr_for_each_hand = np.argmax(ev_br_all_actions[(:, plyr)], axis=0)
    node.ev_weighted = (node.ev * node.reach_probs)
    node.ev_br_weighted = (node.ev_br * node.reach_probs)
    assert np.allclose(np.sum(node.ev_weighted), 0, atol=0.001), np.sum(node.ev_weighted)
    node.epsilon = (node.ev_br_weighted - node.ev_weighted)
    node.exploitability = np.sum(node.epsilon, axis=1)
