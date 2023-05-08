import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F


def __init__(self, fixconvs=False, nopretrained=True):
    super(C3D, self).__init__()
    self.conv1 = nn.Conv3d(3, 64, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.pool1 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2))
    self.conv2 = nn.Conv3d(64, 128, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))
    self.conv3a = nn.Conv3d(128, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.conv3b = nn.Conv3d(256, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.pool3 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))
    self.conv4a = nn.Conv3d(256, 512, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.conv4b = nn.Conv3d(512, 512, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.pool4 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))
    self.conv5a = nn.Conv3d(512, 512, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.conv5b = nn.Conv3d(512, 512, kernel_size=(3, 3, 3), padding=(1, 1, 1))
    self.pool5 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2), padding=(0, 1, 1))
    self.fc6 = nn.Linear(8192, 4096)
    self.fc7 = nn.Linear(4096, 4096)
    self.fc8 = nn.Linear(4096, 487)
    self.dropout = nn.Dropout(p=0.1)
    self.relu = nn.ReLU()
    self.softmax = nn.Softmax()
    if nopretrained:
        self.load_state_dict(torch.load('/workplace/c3d.pickle'))
    self.regressor = nn.Linear(4096, 300)
    if fixconvs:
        for model in [self.conv1, self.conv2, self.conv3a, self.conv3b, self.conv4a, self.conv4b, self.conv5a, self.conv5b, self.fc6]:
            for param in model.parameters():
                param.requires_grad = False
