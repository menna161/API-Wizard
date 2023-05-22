from torch import nn
from mmdet.utils import build_from_cfg
from .registry import BACKBONES, DETECTORS, HEADS, LOSSES, NECKS, ROI_EXTRACTORS, SHARED_HEADS


def build(cfg, registry, default_args=None):
    if isinstance(cfg, list):
        modules = [build_from_cfg(cfg_, registry, default_args) for cfg_ in cfg]
        return nn.Sequential(*modules)
    else:
        return build_from_cfg(cfg, registry, default_args)
