import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
from torchvision.transforms import Compose
from dataset.dense_transform import Normalize, Rotate90, VFlip, Pad, RandomRotate
from dataset.dense_transform import RandomCropAndScale, HFlip, ToTensor, ColorJitterImage, LightingImage
from tools.adamw import AdamW
from tools.clr import CyclicLR
from tools.lr_policy import PolyLR


def create_optimizer(optimizer_config, model, master_params=None):
    'Creates optimizer and schedule from configuration\n\n    Parameters\n    ----------\n    optimizer_config : dict\n        Dictionary containing the configuration options for the optimizer.\n    model : Model\n        The network model.\n\n    Returns\n    -------\n    optimizer : Optimizer\n        The optimizer.\n    scheduler : LRScheduler\n        The learning rate scheduler.\n    '
    if (optimizer_config['classifier_lr'] != (- 1)):
        net_params = []
        classifier_params = []
        for (k, v) in model.named_parameters():
            if (not v.requires_grad):
                continue
            if (k.find('encoder') != (- 1)):
                net_params.append(v)
            else:
                classifier_params.append(v)
        params = [{'params': net_params}, {'params': classifier_params, 'lr': optimizer_config['classifier_lr']}]
    elif master_params:
        params = master_params
    else:
        params = model.parameters()
    if (optimizer_config['type'] == 'SGD'):
        optimizer = optim.SGD(params, lr=optimizer_config['learning_rate'], momentum=optimizer_config['momentum'], weight_decay=optimizer_config['weight_decay'], nesterov=optimizer_config['nesterov'])
    elif (optimizer_config['type'] == 'Adam'):
        optimizer = optim.Adam(params, lr=optimizer_config['learning_rate'], weight_decay=optimizer_config['weight_decay'])
    elif (optimizer_config['type'] == 'AdamW'):
        optimizer = AdamW(params, lr=optimizer_config['learning_rate'], weight_decay=optimizer_config['weight_decay'])
    elif (optimizer_config['type'] == 'RmsProp'):
        optimizer = optim.Adam(params, lr=optimizer_config['learning_rate'], weight_decay=optimizer_config['weight_decay'])
    else:
        raise KeyError('unrecognized optimizer {}'.format(optimizer_config['type']))
    if (optimizer_config['schedule']['type'] == 'step'):
        scheduler = lr_scheduler.StepLR(optimizer, **optimizer_config['schedule']['params'])
    elif (optimizer_config['schedule']['type'] == 'multistep'):
        scheduler = lr_scheduler.MultiStepLR(optimizer, **optimizer_config['schedule']['params'])
    elif (optimizer_config['schedule']['type'] == 'exponential'):
        scheduler = lr_scheduler.ExponentialLR(optimizer, **optimizer_config['schedule']['params'])
    elif (optimizer_config['schedule']['type'] == 'poly'):
        scheduler = PolyLR(optimizer, **optimizer_config['schedule']['params'])
    elif (optimizer_config['schedule']['type'] == 'clr'):
        scheduler = CyclicLR(optimizer, **optimizer_config['schedule']['params'])
    elif (optimizer_config['schedule']['type'] == 'constant'):
        scheduler = lr_scheduler.LambdaLR(optimizer, (lambda epoch: 1.0))
    elif (optimizer_config['schedule']['type'] == 'linear'):

        def linear_lr(it):
            return ((it * optimizer_config['schedule']['params']['alpha']) + optimizer_config['schedule']['params']['beta'])
        scheduler = lr_scheduler.LambdaLR(optimizer, linear_lr)
    return (optimizer, scheduler)
