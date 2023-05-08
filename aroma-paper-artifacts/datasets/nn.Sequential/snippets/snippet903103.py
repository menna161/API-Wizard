from __future__ import absolute_import, division, print_function, unicode_literals
import abc
import sys
import numpy as np
import logging as logger
import torch
import torch
import torch
import torch
import torch
import os
import torch
import time
import copy
import os
import torch
import torch.nn as nn
import torch.nn as nn
import torch.nn as nn


@property
def layer_names(self):
    '\n        Return the hidden layers in the model, if applicable.\n\n        :return: The hidden layers in the model, input and output layers excluded.\n        :rtype: `list`\n\n        .. warning:: `layer_names` tries to infer the internal structure of the model.\n                     This feature comes with no guarantees on the correctness of the result.\n                     The intended order of the layers tries to match their order in the model, but this is not\n                     guaranteed either. In addition, the function can only infer the internal layers if the input\n                     model is of type `nn.Sequential`, otherwise, it will only return the logit layer.\n        '
    return self._layer_names
