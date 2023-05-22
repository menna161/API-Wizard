import torch
import torchvision.transforms as transforms
from pytracking import TensorDict
import ltr.data.processing_utils as prutils
import ltr.data.bounding_box_utils as bbutils
import numpy as np


def _get_jittered_box(self, box, mode):
    jittered_size = (box[2:4] * torch.exp((torch.randn(2) * self.scale_jitter_factor[mode])))
    max_offset = (jittered_size.prod().sqrt() * self.center_jitter_factor[mode]).item()
    jittered_center = ((box[0:2] + (0.5 * box[2:4])) + (max_offset * (torch.rand(2) - 0.5)))
    return torch.cat(((jittered_center - (0.5 * jittered_size)), jittered_size), dim=0)
