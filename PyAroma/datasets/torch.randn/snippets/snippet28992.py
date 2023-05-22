import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import defaultdict
from nbdt.tree import Node, Tree
from nbdt.model import HardEmbeddedDecisionRules, SoftEmbeddedDecisionRules
from math import log
from nbdt.utils import Colors, dataset_to_default_path_graph, dataset_to_default_path_wnids, hierarchy_to_path_graph, coerce_tensor, uncoerce_tensor
from pathlib import Path
import os


@staticmethod
def assert_output_not_nbdt(outputs):
    "\n        >>> x = torch.randn(1, 3, 224, 224)\n        >>> TreeSupLoss.assert_output_not_nbdt(x)  # all good!\n        >>> x._nbdt_output_flag = True\n        >>> TreeSupLoss.assert_output_not_nbdt(x)  #doctest: +ELLIPSIS\n        Traceback (most recent call last):\n            ...\n        AssertionError: ...\n        >>> from nbdt.model import NBDT\n        >>> import torchvision.models as models\n        >>> model = models.resnet18()\n        >>> y = model(x)\n        >>> TreeSupLoss.assert_output_not_nbdt(y)  # all good!\n        >>> model = NBDT('CIFAR10', model, arch='ResNet18')\n        >>> y = model(x)\n        >>> TreeSupLoss.assert_output_not_nbdt(y)  #doctest: +ELLIPSIS\n        Traceback (most recent call last):\n            ...\n        AssertionError: ...\n        "
    assert (getattr(outputs, '_nbdt_output_flag', False) is False), "Uh oh! Looks like you passed an NBDT model's output to an NBDT loss. NBDT losses are designed to take in the *original* model's outputs, as input. NBDT models are designed to only be used during validation and inference, not during training. Confused?  Check out github.com/alvinwan/nbdt#convert-neural-networks-to-decision-trees for examples and instructions."
