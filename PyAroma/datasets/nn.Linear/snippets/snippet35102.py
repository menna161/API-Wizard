import paddle.fluid as fluid
import paddle.fluid.dygraph.nn as nn
import paddle.fluid.layers as L
from utils import model_size, build_norm_layer, build_conv_layer
from models.resnet import ResNet
from models.triple_loss import TripletLoss


def __init__(self, backbone, neck, head, train_cfg=None, test_cfg=None, pretrained=None):
    super(Classifier, self).__init__()
    self.dropout = backbone.pop('dropout')
    self.backbone = ResNet(**backbone)
    self.train_cfg = train_cfg
    self.test_cfg = test_cfg
    self.triple_loss = TripletLoss()
    self.avgpool = nn.Pool2D(pool_type='avg', global_pooling=True)
    self.fc = nn.Linear(512, 2, act='softmax')
    self.init_weights(pretrained=pretrained)
