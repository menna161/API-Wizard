import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Parameter


def forward(self, x, init=False):
    if (init is True):
        self.V.data.copy_((torch.randn(self.V.data.size()).type_as(self.V.data) * 0.05))
        v_norm = (self.V.data / self.V.data.view(self.out_channels, (- 1)).norm(2, 1).view(self.out_channels, *([1] * (len(self.kernel_size) + 1))).expand_as(self.V.data))
        x_init = F.conv2d(x, v_norm, None, self.stride, self.padding, self.dilation, self.groups).data
        t_x_init = x_init.transpose(0, 1).contiguous().view(self.out_channels, (- 1))
        (m_init, v_init) = (t_x_init.mean(1).squeeze(1), t_x_init.var(1).squeeze(1))
        scale_init = (self.init_scale / torch.sqrt((v_init + 1e-10)))
        self.g.data.copy_(scale_init)
        self.b.data.copy_(((- m_init) * scale_init))
        scale_init_shape = scale_init.view(1, self.out_channels, *([1] * (len(x_init.size()) - 2)))
        m_init_shape = m_init.view(1, self.out_channels, *([1] * (len(x_init.size()) - 2)))
        x_init = (scale_init_shape.expand_as(x_init) * (x_init - m_init_shape.expand_as(x_init)))
        self.V_avg.copy_(self.V.data)
        self.g_avg.copy_(self.g.data)
        self.b_avg.copy_(self.b.data)
        return x_init
    else:
        (v, g, b) = get_vars_maybe_avg(self, ['V', 'g', 'b'], self.training, polyak_decay=self.polyak_decay)
        scalar = torch.norm(v.view(self.out_channels, (- 1)), 2, 1)
        if (len(scalar.size()) == 2):
            scalar = (g / scalar.squeeze(1))
        else:
            scalar = (g / scalar)
        w = (scalar.view(self.out_channels, *([1] * (len(v.size()) - 1))).expand_as(v) * v)
        x = F.conv2d(x, w, b, self.stride, self.padding, self.dilation, self.groups)
        return x
