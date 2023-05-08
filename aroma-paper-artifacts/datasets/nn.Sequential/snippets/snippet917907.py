from copy import deepcopy
from nnunet.utilities.nd_softmax import softmax_helper
from torch import nn
import torch
import numpy as np
from nnunet.network_architecture.initialization import InitWeights_He
from nnunet.network_architecture.neural_network import SegmentationNetwork
import torch.nn.functional


def __init__(self, input_channels, base_num_features, num_classes, num_pool, num_conv_per_stage=2, feat_map_mul_on_downscale=2, conv_op=nn.Conv2d, norm_op=nn.BatchNorm2d, norm_op_kwargs=None, dropout_op=nn.Dropout2d, dropout_op_kwargs=None, nonlin=nn.LeakyReLU, nonlin_kwargs=None, deep_supervision=True, dropout_in_localization=False, final_nonlin=softmax_helper, weightInitializer=InitWeights_He(0.01), pool_op_kernel_sizes=None, conv_kernel_sizes=None, upscale_logits=False, convolutional_pooling=False, convolutional_upsampling=False, max_num_features=None, basic_block=ConvDropoutNormNonlin, seg_output_use_bias=False):
    '\n        basically more flexible than v1, architecture is the same\n\n        Does this look complicated? Nah bro. Functionality > usability\n\n        This does everything you need, including world peace.\n\n        Questions? -> f.isensee@dkfz.de\n        '
    super(Generic_UNet, self).__init__()
    self.convolutional_upsampling = convolutional_upsampling
    self.convolutional_pooling = convolutional_pooling
    self.upscale_logits = upscale_logits
    if (nonlin_kwargs is None):
        nonlin_kwargs = {'negative_slope': 0.01, 'inplace': True}
    if (dropout_op_kwargs is None):
        dropout_op_kwargs = {'p': 0.5, 'inplace': True}
    if (norm_op_kwargs is None):
        norm_op_kwargs = {'eps': 1e-05, 'affine': True, 'momentum': 0.1}
    self.conv_kwargs = {'stride': 1, 'dilation': 1, 'bias': True}
    self.nonlin = nonlin
    self.nonlin_kwargs = nonlin_kwargs
    self.dropout_op_kwargs = dropout_op_kwargs
    self.norm_op_kwargs = norm_op_kwargs
    self.weightInitializer = weightInitializer
    self.conv_op = conv_op
    self.norm_op = norm_op
    self.dropout_op = dropout_op
    self.num_classes = num_classes
    self.final_nonlin = final_nonlin
    self._deep_supervision = deep_supervision
    self.do_ds = deep_supervision
    if (conv_op == nn.Conv2d):
        upsample_mode = 'bilinear'
        pool_op = nn.MaxPool2d
        transpconv = nn.ConvTranspose2d
        if (pool_op_kernel_sizes is None):
            pool_op_kernel_sizes = ([(2, 2)] * num_pool)
        if (conv_kernel_sizes is None):
            conv_kernel_sizes = ([(3, 3)] * (num_pool + 1))
    elif (conv_op == nn.Conv3d):
        upsample_mode = 'trilinear'
        pool_op = nn.MaxPool3d
        transpconv = nn.ConvTranspose3d
        if (pool_op_kernel_sizes is None):
            pool_op_kernel_sizes = ([(2, 2, 2)] * num_pool)
        if (conv_kernel_sizes is None):
            conv_kernel_sizes = ([(3, 3, 3)] * (num_pool + 1))
    else:
        raise ValueError(('unknown convolution dimensionality, conv op: %s' % str(conv_op)))
    self.input_shape_must_be_divisible_by = np.prod(pool_op_kernel_sizes, 0, dtype=np.int64)
    self.pool_op_kernel_sizes = pool_op_kernel_sizes
    self.conv_kernel_sizes = conv_kernel_sizes
    self.conv_pad_sizes = []
    for krnl in self.conv_kernel_sizes:
        self.conv_pad_sizes.append([(1 if (i == 3) else 0) for i in krnl])
    if (max_num_features is None):
        if (self.conv_op == nn.Conv3d):
            self.max_num_features = self.MAX_NUM_FILTERS_3D
        else:
            self.max_num_features = self.MAX_FILTERS_2D
    else:
        self.max_num_features = max_num_features
    self.conv_blocks_context = []
    self.conv_blocks_localization = []
    self.td = []
    self.tu = []
    self.seg_outputs = []
    output_features = base_num_features
    input_features = input_channels
    for d in range(num_pool):
        if ((d != 0) and self.convolutional_pooling):
            first_stride = pool_op_kernel_sizes[(d - 1)]
        else:
            first_stride = None
        self.conv_kwargs['kernel_size'] = self.conv_kernel_sizes[d]
        self.conv_kwargs['padding'] = self.conv_pad_sizes[d]
        self.conv_blocks_context.append(StackedConvLayers(input_features, output_features, num_conv_per_stage, self.conv_op, self.conv_kwargs, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs, first_stride, basic_block=basic_block))
        if (not self.convolutional_pooling):
            self.td.append(pool_op(pool_op_kernel_sizes[d]))
        input_features = output_features
        output_features = int(np.round((output_features * feat_map_mul_on_downscale)))
        output_features = min(output_features, self.max_num_features)
    if self.convolutional_pooling:
        first_stride = pool_op_kernel_sizes[(- 1)]
    else:
        first_stride = None
    if self.convolutional_upsampling:
        final_num_features = output_features
    else:
        final_num_features = self.conv_blocks_context[(- 1)].output_channels
    self.conv_kwargs['kernel_size'] = self.conv_kernel_sizes[num_pool]
    self.conv_kwargs['padding'] = self.conv_pad_sizes[num_pool]
    self.conv_blocks_context.append(nn.Sequential(StackedConvLayers(input_features, output_features, (num_conv_per_stage - 1), self.conv_op, self.conv_kwargs, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs, first_stride, basic_block=basic_block), StackedConvLayers(output_features, final_num_features, 1, self.conv_op, self.conv_kwargs, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs, basic_block=basic_block)))
    if (not dropout_in_localization):
        old_dropout_p = self.dropout_op_kwargs['p']
        self.dropout_op_kwargs['p'] = 0.0
    for u in range(num_pool):
        nfeatures_from_down = final_num_features
        nfeatures_from_skip = self.conv_blocks_context[(- (2 + u))].output_channels
        n_features_after_tu_and_concat = (nfeatures_from_skip * 2)
        if ((u != (num_pool - 1)) and (not self.convolutional_upsampling)):
            final_num_features = self.conv_blocks_context[(- (3 + u))].output_channels
        else:
            final_num_features = nfeatures_from_skip
        if (not self.convolutional_upsampling):
            self.tu.append(Upsample(scale_factor=pool_op_kernel_sizes[(- (u + 1))], mode=upsample_mode))
        else:
            self.tu.append(transpconv(nfeatures_from_down, nfeatures_from_skip, pool_op_kernel_sizes[(- (u + 1))], pool_op_kernel_sizes[(- (u + 1))], bias=False))
        self.conv_kwargs['kernel_size'] = self.conv_kernel_sizes[(- (u + 1))]
        self.conv_kwargs['padding'] = self.conv_pad_sizes[(- (u + 1))]
        self.conv_blocks_localization.append(nn.Sequential(StackedConvLayers(n_features_after_tu_and_concat, nfeatures_from_skip, (num_conv_per_stage - 1), self.conv_op, self.conv_kwargs, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs, basic_block=basic_block), StackedConvLayers(nfeatures_from_skip, final_num_features, 1, self.conv_op, self.conv_kwargs, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs, basic_block=basic_block)))
    for ds in range(len(self.conv_blocks_localization)):
        self.seg_outputs.append(conv_op(self.conv_blocks_localization[ds][(- 1)].output_channels, num_classes, 1, 1, 0, 1, 1, seg_output_use_bias))
    self.upscale_logits_ops = []
    cum_upsample = np.cumprod(np.vstack(pool_op_kernel_sizes), axis=0)[::(- 1)]
    for usl in range((num_pool - 1)):
        if self.upscale_logits:
            self.upscale_logits_ops.append(Upsample(scale_factor=tuple([int(i) for i in cum_upsample[(usl + 1)]]), mode=upsample_mode))
        else:
            self.upscale_logits_ops.append((lambda x: x))
    if (not dropout_in_localization):
        self.dropout_op_kwargs['p'] = old_dropout_p
    self.conv_blocks_localization = nn.ModuleList(self.conv_blocks_localization)
    self.conv_blocks_context = nn.ModuleList(self.conv_blocks_context)
    self.td = nn.ModuleList(self.td)
    self.tu = nn.ModuleList(self.tu)
    self.seg_outputs = nn.ModuleList(self.seg_outputs)
    if self.upscale_logits:
        self.upscale_logits_ops = nn.ModuleList(self.upscale_logits_ops)
    if (self.weightInitializer is not None):
        self.apply(self.weightInitializer)