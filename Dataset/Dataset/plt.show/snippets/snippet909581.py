import torch
import torch.nn as nn
from math import sqrt
import functools
from experiments.utils import num_params
import importlib
import attgconv
import importlib
import attgconv
import importlib
import attgconv
import importlib
import attgconv
import importlib
import attgconv
import importlib
import attgconv
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttention as ch_RnG
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttention as ch_RnG
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttention as ch_RnG
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttention as ch_RnG
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
from attgconv.attention_layers import fSpatialAttentionGG
from attgconv.attention_layers import fSpatialAttention
import numpy as np
import matplotlib.pyplot as plt


def forward(self, x):
    h = x
    h = self.c1(h)
    for i in range((self.num_blocks - 1)):
        h = self.block_layers[i](h)
        h = self.trans_layers[i](h)
    h = torch.relu(self.bn_out(self.block_layers[(- 1)](h)))
    h = self.c_out(h)
    h = self.pooling(h, kernel_size=h.shape[(- 1)], stride=2, padding=0)
    h = h.mean(dim=2)
    h = h.view(h.size(0), 2)
    if False:
        from attgconv.attention_layers import fSpatialAttentionGG
        from attgconv.attention_layers import fSpatialAttention
        import numpy as np
        import matplotlib.pyplot as plt
        inx = 0
        B = 60
        maps = []
        for m in self.modules():
            if isinstance(m, fSpatialAttention):
                map = m.att_map.cpu().detach()
                inx = map.shape[(- 2)]
                map = map.expand(map.shape[0], 4, map.shape[2], map.shape[3]).unsqueeze(1)
                maps.append(map)
        upsample = torch.nn.UpsamplingBilinear2d(size=inx)
        for m in self.modules():
            if isinstance(m, fSpatialAttentionGG):
                map = m.att_map.cpu().detach()
                map = map.reshape(map.shape[0], 4, map.shape[(- 2)], map.shape[(- 1)])
                map = upsample(map)
                map = map.reshape(map.shape[0], 1, 4, map.shape[(- 2)], map.shape[(- 1)])
                maps.append(map)
        map_0 = maps[0]
        for i in range((len(maps) - 1)):
            map_0 = (map_0 * maps[(i + 1)])
        plt.figure()
        plt.imshow(map_0.sum((- 3))[(B, 0)])
        plt.show()
        cmap = plt.cm.jet
        time_samples = 4
        scale = 10
        z = np.zeros([inx, inx])
        plt.figure(dpi=600)
        for t in range(4):
            plt.imshow(map_0.sum((- 3))[(B, 0)])
            if (t == 0):
                plt.quiver(z, map_0[(B, 0, t, :, :)], color='red', label='$0^{\\circ}$', scale=scale)
            if (t == 2):
                plt.quiver(z, (- map_0[(B, 0, t, :, :)]), color=cmap((t / time_samples)), label='$180^{\\circ}$', scale=scale)
            if (t == 1):
                plt.quiver((- map_0[(B, 0, t, :, :)]), z, color='cyan', label='$90^{\\circ}$', scale=scale)
            if (t == 3):
                plt.quiver(map_0[(B, 0, t, :, :)], z, color=cmap((t / time_samples)), label='$270^{\\circ}$', scale=scale)
        plt.legend(loc='upper right')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    return h
