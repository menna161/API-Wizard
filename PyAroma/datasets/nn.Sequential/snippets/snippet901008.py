import torch
import torch.nn as nn


def __init__(self):
    super(SimpleUnet, self).__init__()
    self.conv1_block = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.max1 = nn.MaxPool2d(kernel_size=2, stride=2)
    self.conv2_block = nn.Sequential(nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.max2 = nn.MaxPool2d(kernel_size=2, stride=2)
    self.conv3_block = nn.Sequential(nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.max3 = nn.MaxPool2d(kernel_size=2, stride=2)
    self.conv4_block = nn.Sequential(nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.max4 = nn.MaxPool2d(kernel_size=2, stride=2)
    self.conv5_block = nn.Sequential(nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.up_1 = nn.ConvTranspose2d(in_channels=512, out_channels=256, kernel_size=2, stride=2)
    self.conv_up_1 = nn.Sequential(nn.Conv2d(in_channels=512, out_channels=256, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.up_2 = nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=2, stride=2)
    self.conv_up_2 = nn.Sequential(nn.Conv2d(in_channels=256, out_channels=128, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.up_3 = nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=2, stride=2)
    self.conv_up_3 = nn.Sequential(nn.Conv2d(in_channels=128, out_channels=64, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.up_4 = nn.ConvTranspose2d(in_channels=64, out_channels=32, kernel_size=2, stride=2)
    self.conv_up_4 = nn.Sequential(nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True), nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=0, stride=1), nn.ReLU(inplace=True))
    self.conv_final = nn.Conv2d(in_channels=32, out_channels=2, kernel_size=1, padding=0, stride=1)
