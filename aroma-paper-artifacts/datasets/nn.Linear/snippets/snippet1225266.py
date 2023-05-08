import torch
from torch import nn
from torch.autograd import Variable
from torch.nn.parameter import Parameter
from torch._utils import _flatten_dense_tensors, _unflatten_dense_tensors
from .loss_scaler import DynamicLossScaler, LossScaler
from .fp16util import model_grads_to_master_grads, master_params_to_model_params, clip_grad_norm


def load_state_dict(self, state_dict):
    '\n        Loads a state_dict created by an earlier call to state_dict(). \n        If ``fp16_optimizer_instance`` was constructed from some ``init_optimizer``, \n        whose parameters in turn came from ``model``, it is expected that the user \n        will call ``model.load_state_dict()`` before\n        ``fp16_optimizer_instance.load_state_dict()`` is called.\n\n        Example::\n\n            model = torch.nn.Linear(D_in, D_out).cuda().half()\n            optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)\n            optimizer = FP16_Optimizer(optimizer, static_loss_scale = 128.0)\n            ...\n            checkpoint = torch.load("saved.pth")\n            model.load_state_dict(checkpoint[\'model\'])\n            optimizer.load_state_dict(checkpoint[\'optimizer\'])\n        '
    self.loss_scaler = state_dict['loss_scaler']
    self.dynamic_loss_scale = state_dict['dynamic_loss_scale']
    self.overflow = state_dict['overflow']
    self.first_closure_call_this_step = state_dict['first_closure_call_this_step']
    self.optimizer.load_state_dict(state_dict['optimizer_state_dict'])
    for (current_group, saved_group) in zip(self.fp32_from_fp16_groups, state_dict['fp32_from_fp16']):
        for (current, saved) in zip(current_group, saved_group):
            current.data.copy_(saved.data)
