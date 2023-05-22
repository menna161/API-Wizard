import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def forward(self, embedding, triplets):
    e1 = triplets[(:, 0)]
    e2 = triplets[(:, 2)]
    rel = triplets[(:, 1)]
    batch_size = len(triplets)
    e1_embedded = embedding[e1]
    e2_embedded = embedding[e2]
    rel_embedded = self.w_relation(rel)
    stacked_inputs = torch.stack([e1_embedded, rel_embedded, e2_embedded])
    x = self.inp_drop(stacked_inputs)
    x = self.conv1(x.transpose(0, 1))
    x = self.bn1(x)
    x = F.relu(x)
    x = self.feature_map_drop(x)
    x = x.view(batch_size, (- 1))
    x = self.fc(x)
    x = self.hidden_drop(x)
    x = self.bn2(x)
    x = F.relu(x)
    pred = torch.sigmoid(x)
    return pred.squeeze(1)
