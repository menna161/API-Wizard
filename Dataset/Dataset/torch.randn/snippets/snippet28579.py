import torch
from torch.autograd import Function
from torch.nn.modules.utils import _pair
from lib.sa.functions.utils import Dtype, Stream, load_kernel
import os
from functools import partial


def test_subtraction_refpad():
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    (kernel_size, stride, dilation) = (5, 4, 2)
    padding = (((dilation * (kernel_size - 1)) + 1) // 2)
    (n, c, in_height, in_width) = (2, 8, 5, 5)
    out_height = int(((((in_height + (2 * padding)) - ((dilation * (kernel_size - 1)) + 1)) / stride) + 1))
    out_width = int(((((in_width + (2 * padding)) - ((dilation * (kernel_size - 1)) + 1)) / stride) + 1))
    x = torch.randn(n, c, in_height, in_width, requires_grad=True).double().cuda()
    y1 = subtraction_refpad(x, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation)
    unfold_i = torch.nn.Unfold(kernel_size=1, dilation=dilation, padding=0, stride=stride)
    unfold_j = torch.nn.Unfold(kernel_size=kernel_size, dilation=dilation, padding=0, stride=stride)
    pad = torch.nn.ReflectionPad2d(padding)
    y2 = (unfold_i(x).view(n, c, 1, (out_height * out_width)) - unfold_j(pad(x)).view(n, c, pow(kernel_size, 2), (out_height * out_width)))
    assert ((y1 - y2).abs().max() < 1e-09)
    gx1 = torch.autograd.grad(y1.mean(), x, retain_graph=True)[0]
    gx2 = torch.autograd.grad(y2.mean(), x, retain_graph=True)[0]
    assert ((gx1 - gx2).abs().max() < 1e-09)
    from functools import partial
    assert torch.autograd.gradcheck(partial(subtraction_refpad, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation), x)
    print('test case passed')
