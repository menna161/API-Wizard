import unittest
import functools as ft
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, ALWAYS_HALF, ALWAYS_FLOAT, MATCH_INPUT


def train_eval_train_test(self, module, t):
    model = module(t).cuda()
    dummy_optimizer = torch.optim.SGD(model.parameters(), lr=1.0)

    def training_step():
        for param in model.parameters():
            param.grad = None
        loss = model(self.x).sum()
        self.handle._default_scaler._loss_scale = 1.0
        with self.handle.scale_loss(loss, dummy_optimizer) as scaled_loss:
            scaled_loss.backward()
        self.assertEqual(len([p.grad for p in model.parameters() if (p.grad is not None)]), 1)
        self.assertEqual(model.weight.grad.type(), model.weight.type())
        reference_grad = get_reference_grad(self.x, model.weight, model.ops)
        if (model.weight.grad.type() == 'torch.cuda.HalfTensor'):
            self.assertTrue(torch.allclose(model.weight.grad.float(), reference_grad))
        elif (model.weight.grad.type() == 'torch.cuda.FloatTensor'):
            self.assertTrue(torch.allclose(model.weight.grad.float(), reference_grad))
        else:
            raise RuntimeError('model.weight.grad.type = {}'.format(model.weight.grad.type()))
        model.weight.data -= 1.0
    training_step()
    with torch.no_grad():
        loss = model(self.x).sum()
    training_step()
