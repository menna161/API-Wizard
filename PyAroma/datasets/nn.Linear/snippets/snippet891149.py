import numpy as np
import torch
import torch.nn as nn


def __init__(self, env_bldr, device, mpm_args):
    super().__init__()
    self.args = mpm_args
    self.env_bldr = env_bldr
    self.N_SEATS = self.env_bldr.N_SEATS
    self.device = device
    self.board_start = self.env_bldr.obs_board_idxs[0]
    self.board_stop = (self.board_start + len(self.env_bldr.obs_board_idxs))
    self.pub_obs_size = self.env_bldr.pub_obs_size
    self.priv_obs_size = self.env_bldr.priv_obs_size
    self._relu = nn.ReLU(inplace=False)
    if mpm_args.use_pre_layers:
        self._priv_cards = nn.Linear(in_features=self.env_bldr.priv_obs_size, out_features=mpm_args.other_units)
        self._board_cards = nn.Linear(in_features=self.env_bldr.obs_size_board, out_features=mpm_args.other_units)
        self.cards_fc_1 = nn.Linear(in_features=(2 * mpm_args.other_units), out_features=mpm_args.card_block_units)
        self.cards_fc_2 = nn.Linear(in_features=mpm_args.card_block_units, out_features=mpm_args.card_block_units)
        self.cards_fc_3 = nn.Linear(in_features=mpm_args.card_block_units, out_features=mpm_args.other_units)
        self.hist_and_state_1 = nn.Linear(in_features=(self.env_bldr.pub_obs_size - self.env_bldr.obs_size_board), out_features=mpm_args.other_units)
        self.hist_and_state_2 = nn.Linear(in_features=mpm_args.other_units, out_features=mpm_args.other_units)
        self.final_fc_1 = nn.Linear(in_features=(2 * mpm_args.other_units), out_features=mpm_args.other_units)
        self.final_fc_2 = nn.Linear(in_features=mpm_args.other_units, out_features=mpm_args.other_units)
    else:
        self.final_fc_1 = nn.Linear(in_features=self.env_bldr.complete_obs_size, out_features=mpm_args.other_units)
        self.final_fc_2 = nn.Linear(in_features=mpm_args.other_units, out_features=mpm_args.other_units)
    self.lut_range_idx_2_priv_o = torch.from_numpy(self.env_bldr.lut_holder.LUT_RANGE_IDX_TO_PRIVATE_OBS)
    self.lut_range_idx_2_priv_o = self.lut_range_idx_2_priv_o.to(device=self.device, dtype=torch.float32)
    self.to(device)
