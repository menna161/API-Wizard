import operator as op
from typing import Union, Tuple
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable


def __call__(self, model, inputs, targets, device, to_numpy=False):
    '\n        Produce adversarial examples for ``inputs``.\n\n        :param model: the model to attack\n        :type model: nn.Module\n        :param inputs: the original images tensor, of dimension [B x C x H x W].\n               ``inputs`` can be on either CPU or GPU, but it will eventually be\n               moved to the same device as the one the parameters of ``model``\n               reside\n        :type inputs: torch.FloatTensor\n        :param targets: the original image labels, or the attack targets, of\n               dimension [B]. If ``self.targeted`` is ``True``, then ``targets``\n               is treated as the attack targets, otherwise the labels.\n               ``targets`` can be on either CPU or GPU, but it will eventually\n               be moved to the same device as the one the parameters of\n               ``model`` reside\n        :type targets: torch.LongTensor\n        :param to_numpy: True to return an `np.ndarray`, otherwise,\n               `torch.FloatTensor`\n        :type to_numpy: bool\n        :return: the adversarial examples on CPU, of dimension [B x C x H x W]\n        '
    assert isinstance(model, nn.Module)
    assert (len(inputs.size()) == 4)
    assert (len(targets.size()) == 1)
    targets_np = targets.clone().cpu().numpy()
    num_classes = 2
    batch_size = inputs.size(0)
    lower_bounds_np = np.zeros(batch_size)
    upper_bounds_np = (np.ones(batch_size) * self.c_range[1])
    scale_consts_np = (np.ones(batch_size) * self.c_range[0])
    o_best_l2 = (np.ones(batch_size) * np.inf)
    o_best_l2_ppred = (- np.ones(batch_size))
    o_best_advx = inputs.clone().cpu().numpy()
    inputs_tanh = self._to_tanh_space(inputs)
    inputs_tanh_var = Variable(inputs_tanh, requires_grad=False)
    targets_oh = torch.zeros((targets.size() + (num_classes,)))
    targets_oh = targets_oh.to(device)
    targets_oh.scatter_(1, targets.unsqueeze(1), 1.0)
    targets_oh_var = Variable(targets_oh, requires_grad=False)
    pert_tanh = torch.zeros(inputs.size())
    if self.init_rand:
        nn.init.normal(pert_tanh, mean=0, std=0.001)
    pert_tanh = pert_tanh.to(device)
    pert_tanh_var = Variable(pert_tanh, requires_grad=True)
    optimizer = optim.Adam([pert_tanh_var], lr=self.optimizer_lr)
    for sstep in range(self.binary_search_steps):
        if (self.repeat and (sstep == (self.binary_search_steps - 1))):
            scale_consts_np = upper_bounds_np
        scale_consts = torch.from_numpy(np.copy(scale_consts_np)).float()
        scale_consts = scale_consts.to(device)
        scale_consts_var = Variable(scale_consts, requires_grad=False)
        print('Using scale consts:', list(scale_consts_np))
        best_l2 = (np.ones(batch_size) * np.inf)
        best_l2_ppred = (- np.ones(batch_size))
        prev_batch_loss = np.inf
        for optim_step in range(self.max_steps):
            (batch_loss, pert_norms_np, pert_outputs_np, advxs_np) = self._optimize(model, optimizer, inputs_tanh_var, pert_tanh_var, targets_oh_var, scale_consts_var)
            if ((optim_step % 10) == 0):
                print('batch [{}] loss: {}'.format(optim_step, batch_loss))
            if (self.abort_early and (not (optim_step % (self.max_steps // 10)))):
                if (batch_loss > (prev_batch_loss * (1 - self.ae_tol))):
                    break
                prev_batch_loss = batch_loss
            pert_predictions_np = np.argmax(pert_outputs_np, axis=1)
            comp_pert_predictions_np = np.argmax(self._compensate_confidence(pert_outputs_np, targets_np), axis=1)
            for i in range(batch_size):
                l2 = pert_norms_np[i]
                cppred = comp_pert_predictions_np[i]
                ppred = pert_predictions_np[i]
                tlabel = targets_np[i]
                ax = advxs_np[i]
                if self._attack_successful(cppred, tlabel):
                    assert (cppred == ppred)
                    if (l2 < best_l2[i]):
                        best_l2[i] = l2
                        best_l2_ppred[i] = ppred
                    if (l2 < o_best_l2[i]):
                        o_best_l2[i] = l2
                        o_best_l2_ppred[i] = ppred
                        o_best_advx[i] = ax
        for i in range(batch_size):
            tlabel = targets_np[i]
            assert ((best_l2_ppred[i] == (- 1)) or self._attack_successful(best_l2_ppred[i], tlabel))
            assert ((o_best_l2_ppred[i] == (- 1)) or self._attack_successful(o_best_l2_ppred[i], tlabel))
            if (best_l2_ppred[i] != (- 1)):
                if (scale_consts_np[i] < upper_bounds_np[i]):
                    upper_bounds_np[i] = scale_consts_np[i]
                if (upper_bounds_np[i] < (self.c_range[1] * 0.1)):
                    scale_consts_np[i] = ((lower_bounds_np[i] + upper_bounds_np[i]) / 2)
            else:
                if (scale_consts_np[i] > lower_bounds_np[i]):
                    lower_bounds_np[i] = scale_consts_np[i]
                if (upper_bounds_np[i] < (self.c_range[1] * 0.1)):
                    scale_consts_np[i] = ((lower_bounds_np[i] + upper_bounds_np[i]) / 2)
                else:
                    scale_consts_np[i] *= 10
    if (not to_numpy):
        o_best_advx = torch.from_numpy(o_best_advx).float()
    return o_best_advx
