import torch.nn as nn


def __init__(self, n_classes=4, learned_billinear=False):
    super(section_deconvnet, self).__init__()
    self.learned_billinear = learned_billinear
    self.n_classes = n_classes
    self.unpool = nn.MaxUnpool2d(2, stride=2)
    self.conv_block1 = nn.Sequential(nn.Conv2d(1, 64, 3, padding=1), nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(64, 64, 3, padding=1), nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.MaxPool2d(2, stride=2, return_indices=True, ceil_mode=True))
    self.conv_block2 = nn.Sequential(nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(128, 128, 3, padding=1), nn.BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.MaxPool2d(2, stride=2, return_indices=True, ceil_mode=True))
    self.conv_block3 = nn.Sequential(nn.Conv2d(128, 256, 3, padding=1), nn.BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(256, 256, 3, padding=1), nn.BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(256, 256, 3, padding=1), nn.BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.MaxPool2d(2, stride=2, return_indices=True, ceil_mode=True))
    self.conv_block4 = nn.Sequential(nn.Conv2d(256, 512, 3, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.MaxPool2d(2, stride=2, return_indices=True, ceil_mode=True))
    self.conv_block5 = nn.Sequential(nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.MaxPool2d(2, stride=2, return_indices=True, ceil_mode=True))
    self.conv_block6 = nn.Sequential(nn.Conv2d(512, 4096, 3), nn.BatchNorm2d(4096, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.conv_block7 = nn.Sequential(nn.Conv2d(4096, 4096, 1), nn.BatchNorm2d(4096, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.deconv_block8 = nn.Sequential(nn.ConvTranspose2d(4096, 512, 3, stride=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.unpool_block9 = nn.Sequential(nn.MaxUnpool2d(2, stride=2))
    self.deconv_block10 = nn.Sequential(nn.ConvTranspose2d(512, 512, 3, stride=1, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(512, 512, 3, stride=1, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(512, 512, 3, stride=1, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.unpool_block11 = nn.Sequential(nn.MaxUnpool2d(2, stride=2))
    self.deconv_block12 = nn.Sequential(nn.ConvTranspose2d(512, 512, 3, stride=1, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(512, 512, 3, stride=1, padding=1), nn.BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(512, 256, 3, stride=1, padding=1), nn.BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.unpool_block13 = nn.Sequential(nn.MaxUnpool2d(2, stride=2))
    self.deconv_block14 = nn.Sequential(nn.ConvTranspose2d(256, 256, 3, stride=1, padding=1), nn.BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(256, 256, 3, stride=1, padding=1), nn.BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(256, 128, 3, stride=1, padding=1), nn.BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.unpool_block15 = nn.Sequential(nn.MaxUnpool2d(2, stride=2))
    self.deconv_block16 = nn.Sequential(nn.ConvTranspose2d(128, 128, 3, stride=1, padding=1), nn.BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(128, 64, 3, stride=1, padding=1), nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.unpool_block17 = nn.Sequential(nn.MaxUnpool2d(2, stride=2))
    self.deconv_block18 = nn.Sequential(nn.ConvTranspose2d(64, 64, 3, stride=1, padding=1), nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True), nn.ConvTranspose2d(64, 64, 3, stride=1, padding=1), nn.BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True), nn.ReLU(inplace=True))
    self.seg_score19 = nn.Sequential(nn.Conv2d(64, self.n_classes, 1))
    if self.learned_billinear:
        raise NotImplementedError
