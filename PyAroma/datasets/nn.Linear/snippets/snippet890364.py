import torch
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo


def __init__(self, dataset, depth, alpha, num_classes, bottleneck=False):
    super(PyramidNet, self).__init__()
    self.dataset = dataset
    if self.dataset.startswith('cifar'):
        self.inplanes = 16
        if (bottleneck == True):
            n = int(((depth - 2) / 9))
            block = Bottleneck
        else:
            n = int(((depth - 2) / 6))
            block = BasicBlock
        self.addrate = (alpha / ((3 * n) * 1.0))
        self.input_featuremap_dim = self.inplanes
        self.conv1 = nn.Conv2d(3, self.input_featuremap_dim, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(self.input_featuremap_dim)
        self.featuremap_dim = self.input_featuremap_dim
        self.layer1 = self.pyramidal_make_layer(block, n)
        self.layer2 = self.pyramidal_make_layer(block, n, stride=2)
        self.layer3 = self.pyramidal_make_layer(block, n, stride=2)
        self.final_featuremap_dim = self.input_featuremap_dim
        self.bn_final = nn.BatchNorm2d(self.final_featuremap_dim)
        self.relu_final = nn.ReLU(inplace=True)
        self.avgpool = nn.AvgPool2d(8)
        self.fc = nn.Linear(self.final_featuremap_dim, num_classes)
    elif (dataset == 'imagenet'):
        blocks = {18: BasicBlock, 34: BasicBlock, 50: Bottleneck, 101: Bottleneck, 152: Bottleneck, 200: Bottleneck}
        layers = {18: [2, 2, 2, 2], 34: [3, 4, 6, 3], 50: [3, 4, 6, 3], 101: [3, 4, 23, 3], 152: [3, 8, 36, 3], 200: [3, 24, 36, 3]}
        if (layers.get(depth) is None):
            if (bottleneck == True):
                blocks[depth] = Bottleneck
                temp_cfg = int(((depth - 2) / 12))
            else:
                blocks[depth] = BasicBlock
                temp_cfg = int(((depth - 2) / 8))
            layers[depth] = [temp_cfg, temp_cfg, temp_cfg, temp_cfg]
            print('=> the layer configuration for each stage is set to', layers[depth])
        self.inplanes = 64
        self.addrate = (alpha / (sum(layers[depth]) * 1.0))
        self.input_featuremap_dim = self.inplanes
        self.conv1 = nn.Conv2d(3, self.input_featuremap_dim, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(self.input_featuremap_dim)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.featuremap_dim = self.input_featuremap_dim
        self.layer1 = self.pyramidal_make_layer(blocks[depth], layers[depth][0])
        self.layer2 = self.pyramidal_make_layer(blocks[depth], layers[depth][1], stride=2)
        self.layer3 = self.pyramidal_make_layer(blocks[depth], layers[depth][2], stride=2)
        self.layer4 = self.pyramidal_make_layer(blocks[depth], layers[depth][3], stride=2)
        self.final_featuremap_dim = self.input_featuremap_dim
        self.bn_final = nn.BatchNorm2d(self.final_featuremap_dim)
        self.relu_final = nn.ReLU(inplace=True)
        self.avgpool = nn.AvgPool2d(7)
        self.fc = nn.Linear(self.final_featuremap_dim, num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
