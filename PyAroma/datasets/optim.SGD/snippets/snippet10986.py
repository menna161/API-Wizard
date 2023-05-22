import os
import torch
import torch.backends.cudnn as cudnn
import torch.distributed as dist
from models import backbone
import utils


def __init__(self, params, load_path=None, dist_model=False):
    self.model = backbone.__dict__[params['backbone_arch']](**params['backbone_param'])
    utils.init_weights(self.model, init_type='xavier')
    if (load_path is not None):
        utils.load_weights(load_path, self.model)
    self.model.cuda()
    if dist_model:
        self.model = utils.DistModule(self.model)
        self.world_size = dist.get_world_size()
    else:
        self.model = backbone.FixModule(self.model)
        self.world_size = 1
    if (params['optim'] == 'SGD'):
        self.optim = torch.optim.SGD(self.model.parameters(), lr=params['lr'], momentum=0.9, weight_decay=params['weight_decay'])
    elif (params['optim'] == 'Adam'):
        self.optim = torch.optim.Adam(self.model.parameters(), lr=params['lr'], betas=(params['beta1'], 0.999))
    else:
        raise Exception('No such optimizer: {}'.format(params['optim']))
    cudnn.benchmark = True
