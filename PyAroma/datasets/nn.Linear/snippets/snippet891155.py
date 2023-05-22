import torch
import torch.nn as nn
from PokerRL.rl import rl_util


def __init__(self, env_bldr, device, mpm_args):
    super().__init__()
    self.args = mpm_args
    self.env_bldr = env_bldr
    self.N_SEATS = self.env_bldr.N_SEATS
    self.device = device
    self.board_start = self.env_bldr.obs_board_idxs[0]
    self.board_len = len(self.env_bldr.obs_board_idxs)
    self.table_start = self.env_bldr.obs_table_state_idxs[0]
    self.table_len = len(self.env_bldr.obs_table_state_idxs)
    self.players_info_starts = [player_i_idxs[0] for player_i_idxs in self.env_bldr.obs_players_idxs]
    self.players_info_lens = [len(player_i_idxs) for player_i_idxs in self.env_bldr.obs_players_idxs]
    self.pub_obs_size = self.env_bldr.pub_obs_size
    self.priv_obs_size = self.env_bldr.priv_obs_size
    self._relu = nn.ReLU(inplace=False)
    if mpm_args.use_pre_layers:
        self.cards_fc_1 = nn.Linear(in_features=(self.env_bldr.obs_size_board + self.env_bldr.priv_obs_size), out_features=mpm_args.n_cards_state_units)
        self.cards_fc_2 = nn.Linear(in_features=mpm_args.n_cards_state_units, out_features=mpm_args.n_cards_state_units)
        self.cards_fc_3 = nn.Linear(in_features=mpm_args.n_cards_state_units, out_features=mpm_args.n_cards_state_units)
        self.table_state_fc = nn.Linear(in_features=(self.env_bldr.obs_size_table_state + (self.env_bldr.obs_size_player_info_each * self.N_SEATS)), out_features=mpm_args.n_merge_and_table_layer_units)
        self.merge_fc = nn.Linear(in_features=(mpm_args.n_cards_state_units + mpm_args.n_merge_and_table_layer_units), out_features=mpm_args.n_merge_and_table_layer_units)
        self.rnn = rl_util.str_to_rnn_cls(mpm_args.rnn_cls_str)(input_size=mpm_args.n_merge_and_table_layer_units, hidden_size=mpm_args.rnn_units, num_layers=mpm_args.rnn_stack, dropout=mpm_args.rnn_dropout, bidirectional=False, batch_first=False)
    else:
        ' Inputs all data directly into the rnn. '
        self.rnn = rl_util.str_to_rnn_cls(mpm_args.rnn_cls_str)(input_size=self.env_bldr.complete_obs_size, hidden_size=mpm_args.rnn_units, num_layers=mpm_args.rnn_stack, dropout=mpm_args.rnn_dropout, bidirectional=False, batch_first=False)
    self.lut_range_idx_2_priv_o = torch.from_numpy(self.env_bldr.lut_holder.LUT_RANGE_IDX_TO_PRIVATE_OBS)
    self.lut_range_idx_2_priv_o = self.lut_range_idx_2_priv_o.to(device=self.device, dtype=torch.float32)
    self.to(device)
