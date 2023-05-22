import torch
import torch.nn as nn
import torch.nn.parallel
from torchvision.models import resnet
from utils.pytorch_misc import Flattener
from torchvision.layers import ROIAlign
import torch.utils.model_zoo as model_zoo
from config import USE_IMAGENET_PRETRAINED
from utils.pytorch_misc import pad_sequence
from torch.nn import functional as F
from utils.cvm import RegionCVM


def __init__(self, pretrained=True, average_pool=True, semantic=True, final_dim=1024, layer_fix=True):
    '\n        :param average_pool: whether or not to average pool the representations\n        :param pretrained: Whether we need to load from scratch\n        :param semantic: Whether or not we want to introduce the mask and the class label early on (default Yes)\n        '
    super(SimpleDetector, self).__init__()
    backbone = (_load_resnet_imagenet(pretrained=pretrained) if USE_IMAGENET_PRETRAINED else _load_resnet(pretrained=pretrained))
    self.pre_backbone = nn.Sequential(backbone.conv1, backbone.bn1, backbone.relu, backbone.maxpool, backbone.layer1)
    self.layer2 = backbone.layer2
    self.cvm_2 = RegionCVM(in_channels=(128 * 4), grid=[6, 6])
    self.layer3 = backbone.layer3
    self.cvm_3 = RegionCVM(in_channels=(256 * 4), grid=[4, 4])
    self.roi_align = ROIAlign(((7, 7) if USE_IMAGENET_PRETRAINED else (14, 14)), spatial_scale=(1 / 16), sampling_ratio=0)
    if semantic:
        self.mask_dims = 32
        self.object_embed = torch.nn.Embedding(num_embeddings=81, embedding_dim=128)
        self.mask_upsample = torch.nn.Conv2d(1, self.mask_dims, kernel_size=3, stride=(2 if USE_IMAGENET_PRETRAINED else 1), padding=1, bias=True)
    else:
        self.object_embed = None
        self.mask_upsample = None
    self.layer4 = backbone.layer4
    self.cvm_4 = RegionCVM(in_channels=(512 * 4), grid=[1, 1])
    after_roi_align = []
    self.final_dim = final_dim
    if average_pool:
        after_roi_align += [nn.AvgPool2d(7, stride=1), Flattener()]
    self.after_roi_align = torch.nn.Sequential(*after_roi_align)
    self.obj_downsample = torch.nn.Sequential(torch.nn.Dropout(p=0.1), torch.nn.Linear((2048 + (128 if semantic else 0)), final_dim), torch.nn.ReLU(inplace=True))
    self.regularizing_predictor = torch.nn.Linear(2048, 81)
    for m in self.pre_backbone.modules():
        for p in m.parameters():
            p.requires_grad = False

    def set_bn_fix(m):
        classname = m.__class__.__name__
        if (classname.find('BatchNorm') != (- 1)):
            for p in m.parameters():
                p.requires_grad = False
    self.layer2.apply(set_bn_fix)
    self.layer3.apply(set_bn_fix)
    self.layer4.apply(set_bn_fix)
    if layer_fix:
        for m in self.layer2.modules():
            for p in m.parameters():
                p.requires_grad = False
        for m in self.layer3.modules():
            for p in m.parameters():
                p.requires_grad = False
        for m in self.layer4.modules():
            for p in m.parameters():
                p.requires_grad = False
