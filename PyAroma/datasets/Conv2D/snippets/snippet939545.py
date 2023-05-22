import argparse
import sys
import os
import socket
import numpy as np
import tensorflow as tf
from tensorpack import *
from tensorpack.tfutils import argscope, SmartInit
import horovod.tensorflow as hvd
from imagenet_utils import fbresnet_augmentor, get_val_dataflow, ImageNetModel, eval_classification
from resnet_model import resnet_group, resnet_bottleneck, resnet_backbone, Norm


def get_logits(self, image):
    with argscope([Conv2D, MaxPooling, GlobalAvgPooling, BatchNorm], data_format='NCHW'), argscope(Norm, type=self.norm):
        return resnet_backbone(image, self.num_blocks, resnet_group, resnet_bottleneck)
