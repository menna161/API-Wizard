from copy import deepcopy
from nnunet.network_architecture.custom_modules.helperModules import Identity
from torch import nn


def __init__(self, in_planes, out_planes, kernel_size, props, stride=None):
    '\n        This is the conv bn nonlin conv bn nonlin kind of block\n        :param in_planes:\n        :param out_planes:\n        :param props:\n        :param override_stride:\n        '
    super().__init__()
    self.kernel_size = kernel_size
    props['conv_op_kwargs']['stride'] = 1
    self.stride = stride
    self.props = props
    self.out_planes = out_planes
    self.in_planes = in_planes
    if (stride is not None):
        kwargs_conv1 = deepcopy(props['conv_op_kwargs'])
        kwargs_conv1['stride'] = stride
    else:
        kwargs_conv1 = props['conv_op_kwargs']
    self.conv1 = props['conv_op'](in_planes, out_planes, kernel_size, padding=[((i - 1) // 2) for i in kernel_size], **kwargs_conv1)
    self.norm1 = props['norm_op'](out_planes, **props['norm_op_kwargs'])
    self.nonlin1 = props['nonlin'](**props['nonlin_kwargs'])
    if (props['dropout_op_kwargs']['p'] != 0):
        self.dropout = props['dropout_op'](**props['dropout_op_kwargs'])
    else:
        self.dropout = Identity()
    self.conv2 = props['conv_op'](out_planes, out_planes, kernel_size, padding=[((i - 1) // 2) for i in kernel_size], **props['conv_op_kwargs'])
    self.norm2 = props['norm_op'](out_planes, **props['norm_op_kwargs'])
    self.nonlin2 = props['nonlin'](**props['nonlin_kwargs'])
    if (((self.stride is not None) and any(((i != 1) for i in self.stride))) or (in_planes != out_planes)):
        stride_here = (stride if (stride is not None) else 1)
        self.downsample_skip = nn.Sequential(props['conv_op'](in_planes, out_planes, 1, stride_here, bias=False), props['norm_op'](out_planes, **props['norm_op_kwargs']))
    else:
        self.downsample_skip = (lambda x: x)
