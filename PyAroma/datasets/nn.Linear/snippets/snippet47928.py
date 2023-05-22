from collections import OrderedDict
import torch
import torch.nn as nn


def grow_classifier(device, classifier, class_increment, weight_initializer):
    '\n    Function to grow the units of a classifier an initializing only the newly added units while retaining old knowledge.\n\n    Parameters:\n        device (str): Name of device to use.\n        classifier (torch.nn.module): Trained classifier portion of the model.\n        class_increment (int): Number of classes/units to add.\n        weight_initializer (WeightInit): Weight initializer class instance defining initialization schemes/functions.\n    '
    new_in_features = classifier[(- 1)].in_features
    new_out_features = (classifier[(- 1)].out_features + class_increment)
    bias_flag = False
    tmp_weights = classifier[(- 1)].weight.data.clone()
    if (not isinstance(classifier[(- 1)].bias, type(None))):
        tmp_bias = classifier[(- 1)].bias.data.clone()
        bias_flag = True
    classifier[(- 1)] = nn.Linear(new_in_features, new_out_features, bias=bias_flag)
    classifier[(- 1)].to(device)
    weight_initializer.layer_init(classifier[(- 1)])
    classifier[(- 1)].weight.data[(0:(- class_increment), :)] = tmp_weights
    if (not isinstance(classifier[(- 1)].bias, type(None))):
        classifier[(- 1)].bias.data[0:(- class_increment)] = tmp_bias
