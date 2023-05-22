import paddle.fluid as fluid
import paddle.fluid.dygraph.nn as nn
import paddle.fluid.layers as L
from utils import ConvModule, model_size
from models.resnet import ResNet, BasicBlock, make_res_layer
from models.triple_loss import TripletLoss


def __init__(self, backbone, neck, head, train_cfg=None, test_cfg=None, pretrained=None):
    super(SCAN, self).__init__()
    self.dropout = head.pop('dropout')
    self.backbone = ResNet(**backbone)
    self.neck = DeCoder(**neck)
    self.head = ResNet(**head)
    self.train_cfg = train_cfg
    self.test_cfg = test_cfg
    self.triple_loss = TripletLoss()
    self.avgpool = nn.Pool2D(pool_type='avg', global_pooling=True)
    self.fc = nn.Linear(512, 2, act='softmax')
    self.init_weights(pretrained=pretrained)
