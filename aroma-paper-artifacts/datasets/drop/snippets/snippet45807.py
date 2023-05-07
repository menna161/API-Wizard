import math
import torch
from LeafNATS.modules.attention.attention_multi_head import MultiHeadedAttention
from LeafNATS.modules.utils.LayerNormalization import LayerNormalization
from LeafNATS.modules.utils.PositionwiseFeedForward import PositionwiseFeedForward


def forward(self, input_, mask=None):
    '\n        Transformer\n        '
    hd = self.attentionMH(input_, mask)
    hd = self.norm1((input_ + self.drop(hd)))
    hd = self.norm2((hd + self.layer_ff(hd)))
    return self.drop(hd)
