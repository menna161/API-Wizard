import torch
from torch.autograd import Function
from torch.nn.modules.utils import _pair
from lib.sa.functions.utils import Dtype, Stream, load_kernel
import os
from functools import partial


def test_aggregation_zeropad():
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    (kernel_size, stride, dilation) = (5, 4, 2)
    padding = (((dilation * (kernel_size - 1)) + 1) // 2)
    (n, c_x, c_w, in_height, in_width) = (2, 8, 4, 9, 9)
    out_height = int(((((in_height + (2 * padding)) - ((dilation * (kernel_size - 1)) + 1)) / stride) + 1))
    out_width = int(((((in_width + (2 * padding)) - ((dilation * (kernel_size - 1)) + 1)) / stride) + 1))
    x = torch.randn(n, c_x, in_height, in_width, requires_grad=True).double().cuda()
    w = torch.randn(n, c_w, pow(kernel_size, 2), (out_height * out_width), requires_grad=True).double().cuda()
    y1 = aggregation_zeropad(x, w, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation)
    unfold_j = torch.nn.Unfold(kernel_size=kernel_size, dilation=dilation, padding=padding, stride=stride)
    x2 = unfold_j(x).view(n, (c_x // c_w), c_w, pow(kernel_size, 2), (out_height * out_width))
    y2 = (w.unsqueeze(1) * x2).sum((- 2)).view(n, c_x, out_height, out_width)
    assert ((y1 - y2).abs().max() < 1e-09)
    gx1 = torch.autograd.grad(y1.mean(), x, retain_graph=True)[0]
    gx2 = torch.autograd.grad(y2.mean(), x, retain_graph=True)[0]
    assert ((gx1 - gx2).abs().max() < 1e-09)
    gw1 = torch.autograd.grad(y1.mean(), w, retain_graph=True)[0]
    gw2 = torch.autograd.grad(y2.mean(), w, retain_graph=True)[0]
    assert ((gw1 - gw2).abs().max() < 1e-09)
    from functools import partial
    assert torch.autograd.gradcheck(partial(aggregation_zeropad, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation), (x, w))
    print('test case passed')
