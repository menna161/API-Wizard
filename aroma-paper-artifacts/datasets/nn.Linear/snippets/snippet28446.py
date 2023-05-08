import torch
import torch.nn as nn
from models.CosNormClassifier import CosNorm_Classifier
from utils import *
import pdb


def __init__(self, feat_dim=2048, num_classes=1000):
    super(MetaEmbedding_Classifier, self).__init__()
    self.num_classes = num_classes
    self.fc_hallucinator = nn.Linear(feat_dim, num_classes)
    self.fc_selector = nn.Linear(feat_dim, feat_dim)
    self.cosnorm_classifier = CosNorm_Classifier(feat_dim, num_classes)
