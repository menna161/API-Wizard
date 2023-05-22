import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def evaluate(self, embedding, e1, rel):
    batch_size = e1.shape[0]
    e1_embedded = embedding[e1].view((- 1), 1, 10, 20)
    rel_embedded = self.w_relation(rel).view((- 1), 1, 10, 20)
    stacked_inputs = torch.cat([e1_embedded, rel_embedded], 2)
    stacked_inputs = self.bn0(stacked_inputs)
    x = self.inp_drop(stacked_inputs)
    x = self.conv1(x)
    x = self.bn1(x)
    x = F.relu(x)
    x = self.feature_map_drop(x)
    x = x.view(batch_size, (- 1))
    x = self.fc(x)
    x = self.hidden_drop(x)
    x = self.bn2(x)
    x = F.relu(x)
    x = torch.mm(x, embedding.t())
    x += self.b
    pred = torch.sigmoid(x)
    return pred
