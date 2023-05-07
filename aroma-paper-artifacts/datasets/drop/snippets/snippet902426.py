import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def forward(self, e1, rel, target):
    embedding = self.cur_embedding
    if (not self.no_cuda):
        embedding = embedding.to(torch.cuda.current_device())
    batch_size = e1.shape[0]
    e1 = e1.unsqueeze(1)
    rel = rel.unsqueeze(1)
    e1_embedded = embedding[e1]
    rel_embedded = self.w_relation(rel)
    stacked_inputs = torch.cat([e1_embedded, rel_embedded], 1)
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
    pred = torch.sigmoid(x)
    if (target is None):
        return pred
    else:
        return self.loss(pred, target)
