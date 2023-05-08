import torch.nn as nn
from torch.nn import init


def init_model(self, model):
    '\n        Loops over all convolutional, fully-connexted and batch-normalization\n        layers and calls the layer_init function for each module (layer) in\n        the model to initialize weights and biases for the whole model.\n\n        Parameters:\n            model (torch.nn.Module): Model architecture\n        '
    for m in model.modules():
        if isinstance(m, (nn.Linear, nn.Conv2d)):
            self.layer_init(m)
        elif isinstance(m, (nn.BatchNorm1d, nn.BatchNorm2d)):
            if m.affine:
                m.weight.data.fill_(1)
                m.bias.data.zero_()
