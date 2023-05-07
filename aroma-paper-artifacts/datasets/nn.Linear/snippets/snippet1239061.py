import numbers
import torch
from netdissect.autoeval import autoimport_eval
from netdissect.progress import print_progress
from netdissect.nethook import InstrumentedModel
from netdissect.easydict import EasyDict


def annotate_model_shapes(model, gen=False, imgsize=None):
    assert ((imgsize is not None) or gen)
    if gen:
        first_layer = [c for c in model.modules() if isinstance(c, (torch.nn.Conv2d, torch.nn.ConvTranspose2d, torch.nn.Linear))][0]
        if isinstance(first_layer, (torch.nn.Conv2d, torch.nn.ConvTranspose2d)):
            input_shape = (1, first_layer.in_channels, 1, 1)
        else:
            input_shape = (1, first_layer.in_features)
    else:
        input_shape = ((1, 3) + tuple(imgsize))
    device = next(model.parameters()).device
    dry_run = torch.zeros(input_shape).to(device)
    with torch.no_grad():
        output = model(dry_run)
    model.input_shape = input_shape
    model.feature_shape = {layer: feature.shape for (layer, feature) in model.retained_features().items()}
    model.output_shape = output.shape
    return model
