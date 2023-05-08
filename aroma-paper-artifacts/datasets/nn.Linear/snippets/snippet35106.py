import paddle.fluid as fluid
import paddle.fluid.dygraph.nn as nn
import paddle.fluid.layers as L
from utils import model_size, build_norm_layer, build_conv_layer
from models.resnet import ResNet
from models.triple_loss import TripletLoss


def __init__(self):
    super(ClsLite, self).__init__()
    self.conv_cfg = dict(type='Conv')
    self.norm_cfg = dict(type='BN')
    self._make_stem_layer()
    self.avgpool = nn.Pool2D(pool_type='avg', global_pooling=True)
    self.fc = nn.Linear(128, 2, act='softmax')
