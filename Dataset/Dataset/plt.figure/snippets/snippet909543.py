import torch
import torch.nn as nn
import functools
from experiments.utils import num_params
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
import importlib
import attgconv
from attgconv.attention_layers import fChannelAttention as ch_RnG
from attgconv.attention_layers import fChannelAttentionGG
from attgconv.attention_layers import fSpatialAttention
from attgconv.attention_layers import fSpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import ChannelAttention as ch_RnG
from attgconv.attention_layers import ChannelAttentionGG
from attgconv.attention_layers import SpatialAttention
from attgconv.attention_layers import SpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import ChannelAttention as ch_RnG
from attgconv.attention_layers import ChannelAttentionGG
from attgconv.attention_layers import SpatialAttention
from attgconv.attention_layers import SpatialAttentionGG
import importlib
import attgconv
from attgconv.attention_layers import ChannelAttention as ch_RnG
from attgconv.attention_layers import ChannelAttentionGG
from attgconv.attention_layers import SpatialAttention
from attgconv.attention_layers import SpatialAttentionGG
from attgconv.attention_layers import fSpatialAttentionGG
from attgconv.attention_layers import fSpatialAttention
import numpy as np
import matplotlib.pyplot as plt
from attgconv.attention_layers import fSpatialAttentionGG
from attgconv.attention_layers import fSpatialAttention
import numpy as np
import matplotlib.pyplot as plt


def forward(self, x):
    out = torch.relu(self.bn1(self.c1(self.dp_init(x))))
    out = torch.relu(self.bn2(self.c2(out)))
    if self.really_equivariant:
        out = self.c3(out)
        out = self.pooling(out, kernel_size=2, stride=2, padding=0)
        out = self.dp(torch.relu(self.bn3(out)))
    else:
        out = self.dp(torch.relu(self.bn3(self.c3(out))))
    out = torch.relu(self.bn4(self.c4(out)))
    out = torch.relu(self.bn5(self.c5(out)))
    if self.really_equivariant:
        out = self.c6(out)
        out = self.pooling(out, kernel_size=2, stride=2, padding=0)
        out = self.dp(torch.relu(self.bn6(out)))
    else:
        out = self.dp(torch.relu(self.bn6(self.c6(out))))
    out = torch.relu(self.bn7(self.c7(out)))
    out = torch.relu(self.bn8(self.c8(out)))
    out = torch.relu(self.bn9(self.c9(out)))
    out = torch.nn.functional.avg_pool3d(out, out.size()[2:]).squeeze()
    if False:
        from attgconv.attention_layers import fSpatialAttentionGG
        from attgconv.attention_layers import fSpatialAttention
        import numpy as np
        import matplotlib.pyplot as plt
        inx = 0
        B = 15
        maps = []
        for m in self.modules():
            if isinstance(m, fSpatialAttention):
                map = m.att_map.cpu().detach()
                inx = map.shape[(- 2)]
                map = map.expand(map.shape[0], 8, map.shape[2], map.shape[3]).unsqueeze(1)
                maps.append(map)
        upsample = torch.nn.UpsamplingBilinear2d(size=inx)
        for m in self.modules():
            if isinstance(m, fSpatialAttentionGG):
                map = m.att_map.cpu().detach()
                map = map.reshape(map.shape[0], 8, map.shape[(- 2)], map.shape[(- 1)])
                map = upsample(map)
                map = map.reshape(map.shape[0], 1, 8, map.shape[(- 2)], map.shape[(- 1)])
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
                plt.quiver(z, map_0[(B, 0, t, :, :)], color='red', label='$(1, 0^{\\circ})$', scale=scale)
            if (t == 2):
                plt.quiver(z, (- map_0[(B, 0, t, :, :)]), color=cmap((t / time_samples)), label='$(1, 180^{\\circ})$', scale=scale)
            if (t == 1):
                plt.quiver((- map_0[(B, 0, t, :, :)]), z, color='cyan', label='$(1, 90^{\\circ})$', scale=scale)
            if (t == 3):
                plt.quiver(map_0[(B, 0, t, :, :)], z, color=cmap((t / time_samples)), label='$(1, 270^{\\circ})$', scale=scale)
        plt.legend(loc='upper right')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        cmap = plt.cm.jet
        time_samples = 4
        scale = 10
        z = np.zeros([inx, inx])
        plt.figure(dpi=600)
        for t in range(4, 8, 1):
            plt.imshow(map_0.sum((- 3))[(B, 0)])
            if (t == 0):
                plt.quiver(z, map_0[(B, 0, t, :, :)], color=cmap((t / time_samples)), label='$(-1, 0^{\\circ})$', scale=scale)
            if (t == 2):
                plt.quiver(z, (- map_0[(B, 0, t, :, :)]), color=cmap((t / time_samples)), label='$(-1, 180^{\\circ})$', scale=scale)
            if (t == 1):
                plt.quiver((- map_0[(B, 0, t, :, :)]), z, color=cmap((t / time_samples)), label='$(-1, 90^{\\circ})$', scale=scale)
            if (t == 3):
                plt.quiver(map_0[(B, 0, t, :, :)], z, color=cmap((t / time_samples)), label='$(-1, 270^{\\circ})$', scale=scale)
        plt.legend(loc='upper right')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    return out
