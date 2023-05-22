import torch
import numpy as np
from torch import nn
import torchvision
import torch.nn.functional as F


def __init__(self, num_person=2, device=None):
    self.device = device
    super(Audio_Visual_Fusion, self).__init__()
    self.num_person = num_person
    self.input_dim = ((8 * 257) + (256 * self.num_person))
    self.audio_output = Audio_Model()
    self.video_output = Video_Model()
    self.lstm = nn.LSTM(self.input_dim, 400, num_layers=1, bias=True, batch_first=True, bidirectional=True)
    self.fc1 = nn.Linear(400, 600)
    torch.nn.init.xavier_uniform_(self.fc1.weight)
    self.fc2 = nn.Linear(600, 600)
    torch.nn.init.xavier_uniform_(self.fc2.weight)
    self.fc3 = nn.Linear(600, 600)
    torch.nn.init.xavier_uniform_(self.fc3.weight)
    self.complex_mask_layer = nn.Linear(600, ((2 * 257) * self.num_person))
    torch.nn.init.xavier_uniform_(self.complex_mask_layer.weight)
    self.drop1 = nn.Dropout(0.2)
    self.drop2 = nn.Dropout(0.2)
    self.drop3 = nn.Dropout(0.2)
    self.batch_norm1 = nn.BatchNorm1d(298)
    self.batch_norm2 = nn.BatchNorm1d(298)
    self.batch_norm3 = nn.BatchNorm1d(298)
