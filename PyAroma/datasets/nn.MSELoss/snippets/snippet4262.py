import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from utils.utils import mIoULoss, to_one_hot


def __init__(self, input_size, sad=False, encoder_relu=False, decoder_relu=True, weight_share=True, dataset='CULane'):
    super().__init__()
    (input_w, input_h) = input_size
    self.fc_input_feature = ((5 * int((input_w / 16))) * int((input_h / 16)))
    self.num_classes = (5 if (dataset != 'BDD100K') else 1)
    self.scale_background = 0.4
    self.scale_seg = 1.0
    self.scale_exist = 0.1
    self.scale_sad_seg = 1.0
    self.scale_sad_iou = 0.1
    self.scale_sad_exist = 0.1
    self.scale_sad_distill = 0.1
    self.dataset = dataset
    if (dataset != 'BDD100K'):
        self.ce_loss = nn.CrossEntropyLoss(weight=torch.tensor([self.scale_background, 1, 1, 1, 1]))
        self.bce_loss = nn.BCELoss()
        self.iou_loss = mIoULoss(n_classes=4)
    else:
        self.ce_loss = nn.BCEWithLogitsLoss()
        self.bce_loss = nn.BCELoss()
        self.iou_loss = mIoULoss(n_classes=1)

    def get_encoder_block(n=2):
        seq = nn.Sequential()
        seq.add_module(('regular%d_1' % n), RegularBottleneck(128, padding=1, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('dilated%d_2' % n), RegularBottleneck(128, dilation=2, padding=2, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('asymmetric%d_3' % n), RegularBottleneck(128, kernel_size=5, padding=2, asymmetric=True, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('dilated%d_4' % n), RegularBottleneck(128, dilation=4, padding=4, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('regular%d_5' % n), RegularBottleneck(128, padding=1, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('dilated%d_6' % n), RegularBottleneck(128, dilation=8, padding=8, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('asymmetric%d_7' % n), RegularBottleneck(128, kernel_size=5, asymmetric=True, padding=2, dropout_prob=0.1, relu=encoder_relu))
        seq.add_module(('dilated%d_8' % n), RegularBottleneck(128, dilation=16, padding=16, dropout_prob=0.1, relu=encoder_relu))
        return seq
    self.initial_block = InitialBlock(3, 16, relu=encoder_relu)
    self.sad = sad
    self.downsample1 = DownsamplingBottleneck(16, 64, return_indices=True, dropout_prob=0.01, relu=encoder_relu)
    self.encoder1 = nn.Sequential()
    self.encoder1.add_module('regular1_1', RegularBottleneck(64, padding=1, dropout_prob=0.01, relu=encoder_relu))
    self.encoder1.add_module('regular1_2', RegularBottleneck(64, padding=1, dropout_prob=0.01, relu=encoder_relu))
    self.encoder1.add_module('regular1_3', RegularBottleneck(64, padding=1, dropout_prob=0.01, relu=encoder_relu))
    self.encoder1.add_module('regular1_4', RegularBottleneck(64, padding=1, dropout_prob=0.01, relu=encoder_relu))
    self.downsample2 = DownsamplingBottleneck(64, 128, return_indices=True, dropout_prob=0.1, relu=encoder_relu)
    self.encoder2 = get_encoder_block(n=2)
    self.encoder3 = (self.encoder2 if weight_share else get_encoder_block(3))
    self.encoder4 = (self.encoder2 if weight_share else get_encoder_block(4))
    self.upsample4_0 = UpsamplingBottleneck(256, 64, dropout_prob=0.1, relu=decoder_relu)
    self.regular4_1 = RegularBottleneck(64, padding=1, dropout_prob=0.1, relu=decoder_relu)
    self.regular4_2 = RegularBottleneck(64, padding=1, dropout_prob=0.1, relu=decoder_relu)
    self.upsample5_0 = UpsamplingBottleneck(64, 16, dropout_prob=0.1, relu=decoder_relu)
    self.regular5_1 = RegularBottleneck(16, padding=1, dropout_prob=0.1, relu=decoder_relu)
    self.transposed_conv = nn.ConvTranspose2d(16, self.num_classes, kernel_size=3, stride=2, padding=1, bias=False)
    if self.sad:
        self.at_gen_upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
        self.at_gen_l2_loss = nn.MSELoss(reduction='mean')
    self.exist = nn.Sequential(nn.Conv2d(128, 5, 1), nn.Softmax(dim=1), nn.AvgPool2d(2, 2))
    self.fc = nn.Sequential(nn.Linear(self.fc_input_feature, 128), nn.ReLU(), nn.Linear(128, 4), nn.Sigmoid())
