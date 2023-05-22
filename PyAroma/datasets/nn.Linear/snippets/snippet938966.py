import torch
from extensions.gridding import Gridding, GriddingReverse
from extensions.cubic_feature_sampling import CubicFeatureSampling


def __init__(self, cfg):
    super(GRNet, self).__init__()
    self.gridding = Gridding(scale=64)
    self.conv1 = torch.nn.Sequential(torch.nn.Conv3d(1, 32, kernel_size=4, padding=2), torch.nn.BatchNorm3d(32), torch.nn.LeakyReLU(0.2), torch.nn.MaxPool3d(kernel_size=2))
    self.conv2 = torch.nn.Sequential(torch.nn.Conv3d(32, 64, kernel_size=4, padding=2), torch.nn.BatchNorm3d(64), torch.nn.LeakyReLU(0.2), torch.nn.MaxPool3d(kernel_size=2))
    self.conv3 = torch.nn.Sequential(torch.nn.Conv3d(64, 128, kernel_size=4, padding=2), torch.nn.BatchNorm3d(128), torch.nn.LeakyReLU(0.2), torch.nn.MaxPool3d(kernel_size=2))
    self.conv4 = torch.nn.Sequential(torch.nn.Conv3d(128, 256, kernel_size=4, padding=2), torch.nn.BatchNorm3d(256), torch.nn.LeakyReLU(0.2), torch.nn.MaxPool3d(kernel_size=2))
    self.fc5 = torch.nn.Sequential(torch.nn.Linear(16384, 2048), torch.nn.ReLU())
    self.fc6 = torch.nn.Sequential(torch.nn.Linear(2048, 16384), torch.nn.ReLU())
    self.dconv7 = torch.nn.Sequential(torch.nn.ConvTranspose3d(256, 128, kernel_size=4, stride=2, bias=False, padding=1), torch.nn.BatchNorm3d(128), torch.nn.ReLU())
    self.dconv8 = torch.nn.Sequential(torch.nn.ConvTranspose3d(128, 64, kernel_size=4, stride=2, bias=False, padding=1), torch.nn.BatchNorm3d(64), torch.nn.ReLU())
    self.dconv9 = torch.nn.Sequential(torch.nn.ConvTranspose3d(64, 32, kernel_size=4, stride=2, bias=False, padding=1), torch.nn.BatchNorm3d(32), torch.nn.ReLU())
    self.dconv10 = torch.nn.Sequential(torch.nn.ConvTranspose3d(32, 1, kernel_size=4, stride=2, bias=False, padding=1), torch.nn.BatchNorm3d(1), torch.nn.ReLU())
    self.gridding_rev = GriddingReverse(scale=64)
    self.point_sampling = RandomPointSampling(n_points=2048)
    self.feature_sampling = CubicFeatureSampling()
    self.fc11 = torch.nn.Sequential(torch.nn.Linear(1792, 1792), torch.nn.ReLU())
    self.fc12 = torch.nn.Sequential(torch.nn.Linear(1792, 448), torch.nn.ReLU())
    self.fc13 = torch.nn.Sequential(torch.nn.Linear(448, 112), torch.nn.ReLU())
    self.fc14 = torch.nn.Linear(112, 24)
