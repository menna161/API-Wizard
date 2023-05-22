import numpy as np
import torch
from PokerRL.eval.lbr import _util
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerRange import PokerRange


def _run_no_limit(self, agent_seat_id, n_iterations):
    total_lbr_winnings = np.empty(shape=n_iterations, dtype=np.float32)
    lbr_seat_id = (1 - agent_seat_id)
    n_lbr_bets = len(self._env.bet_sizes_list_as_frac_of_pot)
    for iteration_id in range(n_iterations):
        if ((iteration_id % 50) == 0):
            print('LBR hand: ', iteration_id)
        (env_obs, reward, done, info) = self._reset_episode()
        lbr_hand = self._env.get_hole_cards_of_player(p_id=lbr_seat_id)
        self.agent_range.set_cards_to_zero_prob(cards_2d=lbr_hand)
        while (not done):
            p_id_acting = self._env.current_player.seat_id
            if self.t_prof.DEBUGGING:
                assert (p_id_acting == self.agent.cpu_agent._internal_env_wrapper.env.current_player.seat_id)
            if (p_id_acting == lbr_seat_id):
                if ((self.check_to_round is not None) and (self._env.current_round < self.check_to_round)):
                    action_int = Poker.CHECK_CALL
                else:
                    _rollout_mngr = _LBRRolloutManager(t_prof=self.t_prof, env_bldr=self._eval_env_bldr, env=self._env, lbr_hand_2d=lbr_hand)
                    _utility = np.full(shape=(2 + n_lbr_bets), fill_value=(- 1.0), dtype=np.float32)
                    _utility[Poker.FOLD] = 0.0
                    _wp = _rollout_mngr.get_lbr_checkdown_equity(agent_range=self.agent_range)
                    _asked = (self._env.seats[agent_seat_id].current_bet - self._env.seats[lbr_seat_id].current_bet)
                    _pot_before_action = self._env.get_all_winnable_money()
                    _utility[Poker.CHECK_CALL] = ((_wp * _pot_before_action) - ((1 - _wp) * _asked))
                    _saved_env_state = self._env.state_dict()
                    _saved_agent_env_state = self.agent.env_state_dict()
                    _saved_agent_range_state = self.agent_range.state_dict()
                    _legal_raises = self._env.get_legal_actions()
                    for a in [Poker.FOLD, Poker.CHECK_CALL]:
                        if (a in _legal_raises):
                            _legal_raises.remove(a)
                    for r in _legal_raises:
                        raise_frac = self._env.bet_sizes_list_as_frac_of_pot[(r - 2)]
                        self._env.step(action=r)
                        _pot_after_raise = self._env.get_all_winnable_money()
                        self.agent.notify_of_raise_frac_action(p_id_acted=lbr_seat_id, frac=raise_frac)
                        if self.t_prof.DEBUGGING:
                            assert (agent_seat_id == self.agent.cpu_agent._internal_env_wrapper.env.current_player.seat_id)
                        a_probs_each_hand = self.agent.get_a_probs_for_each_hand()
                        _fold_prob = np.sum((self.agent_range.range * a_probs_each_hand[(:, Poker.FOLD)]))
                        _p_not_fold_per_hand = (1 - a_probs_each_hand[(:, Poker.FOLD)])
                        self.agent_range.mul_and_norm(_p_not_fold_per_hand)
                        _wp_now = _rollout_mngr.get_lbr_checkdown_equity(agent_range=self.agent_range)
                        _chips_lbr_puts_in_pot = (_pot_after_raise - _pot_before_action)
                        _ev_if_fold = _pot_before_action
                        _ev_if_not_fold = ((_wp_now * _pot_after_raise) - ((1 - _wp_now) * _chips_lbr_puts_in_pot))
                        _utility[r] = ((_fold_prob * _ev_if_fold) + ((1 - _fold_prob) * _ev_if_not_fold))
                        self.agent_range.load_state_dict(_saved_agent_range_state)
                        self._env.load_state_dict(_saved_env_state)
                        self.agent.load_env_state_dict(_saved_agent_env_state)
                    action_int = np.argmax(_utility)
                if (action_int >= 2):
                    raise_frac = self._env.bet_sizes_list_as_frac_of_pot[(action_int - 2)]
                    self.agent.notify_of_raise_frac_action(p_id_acted=lbr_seat_id, frac=raise_frac)
                else:
                    self.agent.notify_of_action(p_id_acted=lbr_seat_id, action_he_did=action_int)
            else:
                if self.t_prof.DEBUGGING:
                    assert (p_id_acting == self.agent.cpu_agent._internal_env_wrapper.env.current_player.seat_id)
                (action_int, a_probs_each_hand) = self.agent.get_action(step_env=True, need_probs=True)
                self.agent_range.update_after_action(action=action_int, all_a_probs_for_all_hands=a_probs_each_hand)
                if (action_int >= 2):
                    raise_frac = self.agent.cpu_agent.env_bldr.env_args.bet_sizes_list_as_frac_of_pot[(action_int - 2)]
            old_game_round = self._env.current_round
            if (action_int >= 2):
                (env_obs, reward, done, info) = self._env.step_raise_pot_frac(pot_frac=raise_frac)
            else:
                (env_obs, reward, done, info) = self._env.step(action=action_int)
            if (self._env.current_round != old_game_round):
                self.agent_range.update_after_new_round(new_round=self._env.current_round, board_now_2d=self._env.board)
        total_lbr_winnings[iteration_id] = ((reward[lbr_seat_id] * self._env.REWARD_SCALAR) * self._env.EV_NORMALIZER)
    return total_lbr_winnings
