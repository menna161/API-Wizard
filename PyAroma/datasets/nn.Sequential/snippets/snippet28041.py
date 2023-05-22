import pytorch_lightning as pl
import torch
import torch.nn as nn
from pointnet2_ops.pointnet2_modules import PointnetFPModule, PointnetSAModule
from torch.utils.data import DataLoader
from pointnet2.data import Indoor3DSemSeg
from pointnet2.models.pointnet2_ssg_cls import PointNet2ClassificationSSG


def _build_model(self):
    self.SA_modules = nn.ModuleList()
    self.SA_modules.append(PointnetSAModule(npoint=1024, radius=0.1, nsample=32, mlp=[6, 32, 32, 64], use_xyz=self.hparams['model.use_xyz']))
    self.SA_modules.append(PointnetSAModule(npoint=256, radius=0.2, nsample=32, mlp=[64, 64, 64, 128], use_xyz=self.hparams['model.use_xyz']))
    self.SA_modules.append(PointnetSAModule(npoint=64, radius=0.4, nsample=32, mlp=[128, 128, 128, 256], use_xyz=self.hparams['model.use_xyz']))
    self.SA_modules.append(PointnetSAModule(npoint=16, radius=0.8, nsample=32, mlp=[256, 256, 256, 512], use_xyz=self.hparams['model.use_xyz']))
    self.FP_modules = nn.ModuleList()
    self.FP_modules.append(PointnetFPModule(mlp=[(128 + 6), 128, 128, 128]))
    self.FP_modules.append(PointnetFPModule(mlp=[(256 + 64), 256, 128]))
    self.FP_modules.append(PointnetFPModule(mlp=[(256 + 128), 256, 256]))
    self.FP_modules.append(PointnetFPModule(mlp=[(512 + 256), 256, 256]))
    self.fc_lyaer = nn.Sequential(nn.Conv1d(128, 128, kernel_size=1, bias=False), nn.BatchNorm1d(128), nn.ReLU(True), nn.Dropout(0.5), nn.Conv1d(128, 13, kernel_size=1))
