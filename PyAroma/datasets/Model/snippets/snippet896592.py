import sys
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import BaseFairseqModel, register_model, register_model_architecture


def __init__(self, args):
    super().__init__()
    self.prediction_steps = args.prediction_steps
    offset = args.offset
    if (args.encoder == 'cnn'):
        feature_enc_layers = eval(args.conv_feature_layers)
        self.feature_extractor = ConvFeatureExtractionModel(conv_layers=feature_enc_layers, dropout=0.0, log_compression=args.log_compression, skip_connections=args.skip_connections_feat, residual_scale=args.residual_scale, non_affine_group_norm=args.non_affine_group_norm)
        embed = feature_enc_layers[(- 1)][0]
    else:
        raise Exception(('unknown encoder type ' + args.encoder))
    if (args.offset == 'auto'):
        assert (args.encoder == 'cnn')
        jin = 0
        rin = 0
        for (_, k, stride) in feature_enc_layers:
            if (rin == 0):
                rin = k
            rin = (rin + ((k - 1) * jin))
            if (jin == 0):
                jin = stride
            else:
                jin *= stride
        offset = math.ceil((rin / jin))
    offset = int(offset)

    def make_aggregator():
        if (args.aggregator == 'cnn'):
            agg_layers = eval(args.conv_aggregator_layers)
            agg_dim = agg_layers[(- 1)][0]
            feature_aggregator = ConvAggegator(conv_layers=agg_layers, embed=embed, dropout=args.dropout, skip_connections=args.skip_connections_agg, residual_scale=args.residual_scale, non_affine_group_norm=args.non_affine_group_norm, conv_bias=(not args.no_conv_bias), zero_pad=args.agg_zero_pad)
        elif (args.aggregator == 'gru'):
            agg_dim = args.gru_dim
            feature_aggregator = nn.Sequential(TransposeLast(), nn.GRU(input_size=embed, hidden_size=agg_dim, num_layers=1, dropout=args.dropout), TransposeLast(deconstruct_idx=0))
        else:
            raise Exception(('unknown aggregator type ' + args.aggregator))
        return (feature_aggregator, agg_dim)
    (self.feature_aggregator, agg_dim) = make_aggregator()
    self.wav2vec_predictions = Wav2VecPredictionsModel(in_dim=agg_dim, out_dim=embed, prediction_steps=args.prediction_steps, n_negatives=args.num_negatives, cross_sample_negatives=args.cross_sample_negatives, sample_distance=args.sample_distance, dropout=args.dropout, offset=offset, balanced_classes=args.balanced_classes)
    self.dropout_feats = nn.Dropout(p=args.dropout_features)
    self.dropout_agg = nn.Dropout(p=args.dropout_agg)
    if (args.project_features == 'none'):
        self.project_features = None
    elif (args.project_features == 'same'):
        self.project_features = self.feature_aggregator
    elif (args.project_features == 'new'):
        (self.project_features, _) = make_aggregator()
