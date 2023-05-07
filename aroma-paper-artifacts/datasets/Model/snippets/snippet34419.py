import torch.nn as nn
from torch.nn import init
import resnet


def __init__(self, num_classes, is_3D=True):
    super(A2J_model, self).__init__()
    self.is_3D = is_3D
    self.Backbone = ResNetBackBone()
    self.regressionModel = RegressionModel(2048, num_classes=num_classes)
    self.classificationModel = ClassificationModel(1024, num_classes=num_classes)
    if is_3D:
        self.DepthRegressionModel = DepthRegressionModel(2048, num_classes=num_classes)
