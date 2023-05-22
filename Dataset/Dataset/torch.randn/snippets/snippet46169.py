import torch
import torch.nn as nn
import torch.nn.functional as F
from net.utils.graph import Graph_J, Graph_P, Graph_B
from net.utils.module import *
from net.utils.operation import PartLocalInform, BodyLocalInform


def forward(self, inputs, inputs_previous, inputs_previous2, hidden, t):
    pred_all = []
    res_all = []
    (N, T, D) = inputs.size()
    inputs = inputs.contiguous().view(N, T, self.V, (- 1))
    inputs_previous = inputs_previous.contiguous().view(N, T, self.V, (- 1))
    inputs_previous2 = inputs_previous2.contiguous().view(N, T, self.V, (- 1))
    self.mask = self.mask.view(self.V, 3)
    for step in range(0, t):
        if (step < 1):
            ins_p = inputs[(:, 0, :, :)]
            ins_v = (inputs_previous - inputs_previous2)[(:, 0, :, :)]
            ins_a = ((ins_p - inputs_previous[(:, 0, :, :)]) - ins_v)
            ins_v_dec = (inputs - inputs_previous)[(:, 0, :, :)]
        elif (step == 1):
            ins_p = pred_all[(step - 1)]
            ins_v = (inputs - inputs_previous)[(:, 0, :, :)]
            ins_a = ((ins_p - inputs[(:, 0, :, :)]) - ins_v)
            ins_v_dec = (pred_all[(step - 1)] - inputs[(:, 0, :, :)])
        elif (step == 2):
            ins_p = pred_all[(step - 1)]
            ins_v = (pred_all[(step - 2)] - inputs[(:, 0, :, :)])
            ins_a = ((ins_p - pred_all[(step - 2)]) - ins_v)
            ins_v_dec = (pred_all[(step - 1)] - pred_all[(step - 2)])
        else:
            ins_p = pred_all[(step - 1)]
            ins_v = (pred_all[(step - 2)] - pred_all[(step - 3)])
            ins_a = ((ins_p - pred_all[(step - 2)]) - ins_v)
            ins_v_dec = (pred_all[(step - 1)] - pred_all[(step - 2)])
        n = (torch.randn(ins_p.size()).cuda() * 0.001)
        ins = torch.cat(((ins_p + n), ins_v, ins_a), dim=(- 1))
        (pred_, hidden, res_) = self.step_forward(ins, hidden, step)
        pred_all.append(pred_)
        res_all.append(res_)
    preds = torch.stack(pred_all, dim=1)
    reses = torch.stack(res_all, dim=1)
    preds = (preds * self.mask)
    return preds.transpose(1, 2).contiguous()
