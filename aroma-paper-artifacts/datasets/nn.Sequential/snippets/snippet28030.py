import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim.lr_scheduler as lr_sched
from pointnet2_ops.pointnet2_modules import PointnetFPModule, PointnetSAModule
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import transforms
import pointnet2.data.data_utils as d_utils
from pointnet2.data.ModelNet40Loader import ModelNet40Cls


def _build_model(self):
    self.SA_modules = nn.ModuleList()
    self.SA_modules.append(PointnetSAModule(npoint=512, radius=0.2, nsample=64, mlp=[3, 64, 64, 128], use_xyz=self.hparams['model.use_xyz']))
    self.SA_modules.append(PointnetSAModule(npoint=128, radius=0.4, nsample=64, mlp=[128, 128, 128, 256], use_xyz=self.hparams['model.use_xyz']))
    self.SA_modules.append(PointnetSAModule(mlp=[256, 256, 512, 1024], use_xyz=self.hparams['model.use_xyz']))
    self.fc_layer = nn.Sequential(nn.Linear(1024, 512, bias=False), nn.BatchNorm1d(512), nn.ReLU(True), nn.Linear(512, 256, bias=False), nn.BatchNorm1d(256), nn.ReLU(True), nn.Dropout(0.5), nn.Linear(256, 40))
