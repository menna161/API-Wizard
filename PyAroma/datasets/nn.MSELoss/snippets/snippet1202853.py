import torch.nn as nn
from model import model_original
from model import model_cd


def forward(self, c, iter):
    feats_BE = self.BE.forward_branch(c)
    (*_, feat_SE_aux, feat_SE) = self.SE.forward_aux2(c)
    feats_BD = self.BD.forward_branch(feat_SE_aux)
    feats_SD = self.SD.forward_aux(feat_SE, relu=self.args.updim_relu)
    rec = feats_SD[(- 1)]
    rec_pixl_loss = nn.MSELoss()(rec, c.data)
    rec_feats_BE = self.BE.forward_branch(rec)
    rec_perc_loss = 0
    for i in range(len(rec_feats_BE)):
        rec_perc_loss += nn.MSELoss()(rec_feats_BE[i], feats_BE[i].data)
    kd_feat_loss = 0
    for i in range(len(feats_BD)):
        kd_feat_loss += nn.MSELoss()(feats_SD[i], feats_BD[i].data)
    return (rec_pixl_loss, rec_perc_loss, kd_feat_loss, rec)
