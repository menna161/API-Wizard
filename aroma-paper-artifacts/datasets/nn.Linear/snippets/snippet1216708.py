import torch
import torch.nn as nn
import torchvision
import torch.nn.functional as F


def __init__(self, in_fea):
    super(Graph_reasoning, self).__init__()
    self.hidden_fea = in_fea
    self.hidden_fea_2 = in_fea
    self.final_fea = in_fea
    self.fc_encoder = nn.Linear(in_fea, self.hidden_fea)
    self.fc_o = nn.Linear(self.hidden_fea, self.hidden_fea)
    self.fc_a = nn.Linear(self.hidden_fea, self.hidden_fea)
    self.fc_q = nn.Linear(self.hidden_fea, self.hidden_fea)
    self.fc_o_ = nn.Linear((in_fea + self.hidden_fea), self.hidden_fea)
    self.fc_a_ = nn.Linear(self.hidden_fea, self.hidden_fea)
    self.fc_q_ = nn.Linear((in_fea + self.hidden_fea), self.hidden_fea)
    self.w_s_o = nn.Linear(self.hidden_fea, self.hidden_fea_2)
    self.w_s_a = nn.Linear(self.hidden_fea, self.hidden_fea_2)
    self.w_s_q = nn.Linear(self.hidden_fea, self.hidden_fea_2)
    self.w_s_o_ = nn.Linear(self.hidden_fea, self.hidden_fea_2)
    self.w_s_a_ = nn.Linear(self.hidden_fea, self.hidden_fea_2)
    self.w_s_q_ = nn.Linear(self.hidden_fea, self.hidden_fea_2)
    self.w_g_o = nn.Linear(self.hidden_fea_2, self.final_fea)
    self.w_g_a = nn.Linear(self.hidden_fea_2, self.final_fea)
    self.w_g_q = nn.Linear(self.hidden_fea_2, self.final_fea)
    self.res_w_a = nn.Linear((in_fea * 2), in_fea)
    self.res_w_q = nn.Linear((in_fea * 2), in_fea)
    self.res_w_o = nn.Linear((in_fea * 2), in_fea)
