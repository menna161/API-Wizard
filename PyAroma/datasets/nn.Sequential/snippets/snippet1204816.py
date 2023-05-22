from __future__ import absolute_import
import torch
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, num_input_channels, branches, module_name):
    'Batch, Channel, Width, Height\n        '
    super(ParallelModule, self).__init__()
    if (not isinstance(branches, list)):
        raise ValueError('Unknown parallel module format - expecting list')
    self.parallel_branches = nn.ModuleList()
    self.num_output_channels = 0
    for (branch_idx, branch) in enumerate(branches):
        branch_name = ('%s/b_%d' % (module_name, branch_idx))
        if (not isinstance(branch, list)):
            msg = "Unknown branch format. Module='%s', branch='%s', branch_type='%s'"
            raise ValueError((msg % (module_name, branch_name, type(branch))))
        branch_modules = nn.Sequential()
        num_prev_channels = num_input_channels
        for (op_idx, op) in enumerate(branch):
            op_name = ('%s/op_%d' % (branch_name, op_idx))
            if isinstance(op, list):
                op_module = ParallelModule(num_prev_channels, op, op_name)
                num_prev_channels = op_module.num_output_channels
            elif isinstance(op, tuple):
                if (op[0] == 'conv'):
                    op_module = ConvModule(num_prev_channels, num_filters=op[1], kernel_size=op[2], stride=op[3], padding=op[4])
                    num_prev_channels = op[1]
                elif (op[0] == 'max'):
                    op_module = nn.MaxPool2d(kernel_size=op[1], stride=op[2], padding=op[3])
                elif (op[0] == 'avg'):
                    op_module = nn.AvgPool2d(kernel_size=op[1], stride=op[2], padding=op[3])
                else:
                    raise ValueError(('Unknown operator type (%s)' % op[0]))
            else:
                raise ValueError('Unknown operator format - expecting list or tuple')
            branch_modules.add_module(op_name, op_module)
            self.num_output_channels += num_prev_channels
        self.parallel_branches.append(branch_modules)
