import torch
from torch._utils import _flatten_dense_tensors, _unflatten_dense_tensors
import ctypes


def load_state_dict(self, state_dict):
    '\n        Loads a state_dict created by an earlier call to state_dict(). \n        If ``fp16_optimizer_instance`` was constructed from some ``init_optimizer``, \n        whose parameters in turn came from ``model``, it is expected that the user \n        will call ``model.load_state_dict()`` before\n        ``fp16_optimizer_instance.load_state_dict()`` is called.\n        Example::\n            model = torch.nn.Linear(D_in, D_out).cuda().half()\n            optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)\n            optimizer = FP16_Optimizer(optimizer, static_loss_scale = 128.0)\n            ...\n            checkpoint = torch.load("saved.pth")\n            model.load_state_dict(checkpoint[\'model\'])\n            optimizer.load_state_dict(checkpoint[\'optimizer\'])\n        '
    self.dynamic_loss_scale = state_dict['dynamic_loss_scale']
    self.cur_scale = state_dict['cur_scale']
    self.cur_iter = state_dict['cur_iter']
    if state_dict['dynamic_loss_scale']:
        self.last_overflow_iter = state_dict['last_overflow_iter']
        self.scale_factor = state_dict['scale_factor']
        self.scale_window = state_dict['scale_window']
    self.optimizer.load_state_dict(state_dict['optimizer_state_dict'])
    for (current, saved) in zip(self.fp32_groups_flat, state_dict['fp32_groups_flat']):
        current.data.copy_(saved.data)
