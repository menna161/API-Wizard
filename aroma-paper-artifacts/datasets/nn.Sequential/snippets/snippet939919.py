from model import common
import torch.nn as nn
from model import dilated


def __init__(self, args, conv=common.default_conv):
    super(EDSR, self).__init__()
    n_resblock = args.n_resblocks
    n_feats = args.n_feats
    kernel_size = 3
    scale = args.scale[0]
    act = nn.ReLU(True)
    rgb_mean = (0.4488, 0.4371, 0.404)
    rgb_std = (1.0, 1.0, 1.0)
    self.sub_mean = common.MeanShift(args.rgb_range, rgb_mean, rgb_std)
    m_head = [conv(args.n_colors, n_feats, kernel_size)]
    m_body = [common.ResBlock(conv, n_feats, kernel_size, act=act, res_scale=args.res_scale) for _ in range(n_resblock)]
    m_body.append(conv(n_feats, n_feats, kernel_size))
    m_tail = [common.Upsampler(conv, scale, n_feats, act=False), nn.Conv2d(n_feats, args.n_colors, kernel_size, padding=(kernel_size // 2))]
    self.add_mean = common.MeanShift(args.rgb_range, rgb_mean, rgb_std, 1)
    self.head = nn.Sequential(*m_head)
    self.body = nn.Sequential(*m_body)
    self.tail = nn.Sequential(*m_tail)
