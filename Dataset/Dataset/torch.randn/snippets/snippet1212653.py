import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Parameter


def forward(self, x, init=False):
    if (init is True):
        self.V.data.copy_((torch.randn(self.V.data.size()).type_as(self.V.data) * 0.05))
        v_norm = (self.V.data / self.V.data.norm(2, 1).expand_as(self.V.data))
        x_init = F.linear(x, v_norm).data
        (m_init, v_init) = (x_init.mean(0).squeeze(0), x_init.var(0).squeeze(0))
        scale_init = (self.init_scale / torch.sqrt((v_init + 1e-10)))
        self.g.data.copy_(scale_init)
        self.b.data.copy_(((- m_init) * scale_init))
        x_init = (scale_init.view(1, (- 1)).expand_as(x_init) * (x_init - m_init.view(1, (- 1)).expand_as(x_init)))
        self.V_avg.copy_(self.V.data)
        self.g_avg.copy_(self.g.data)
        self.b_avg.copy_(self.b.data)
        return x_init
    else:
        (v, g, b) = get_vars_maybe_avg(self, ['V', 'g', 'b'], self.training, polyak_decay=self.polyak_decay)
        x = F.linear(x, v)
        scalar = (g / torch.norm(v, 2, 1).squeeze(1))
        x = ((scalar.view(1, (- 1)).expand_as(x) * x) + b.view(1, (- 1)).expand_as(x))
        return x
