import torch.nn as nn
from model import model_original
from model import model_cd


def forward(self, c, iter):
    cF_BE = self.BE.forward_branch(c)
    cF_SE = self.SE.forward_aux(c, self.args.updim_relu)
    rec = self.BD(cF_SE[(- 1)])
    sd_BE = 0
    if ((iter % self.args.save_interval) == 0):
        rec_BE = self.BD(cF_BE[(- 1)])
    feat_loss = 0
    for i in range(len(cF_BE)):
        feat_loss += nn.MSELoss()(cF_SE[i], cF_BE[i].data)
    rec_pixl_loss = nn.MSELoss()(rec, c.data)
    recF_BE = self.BE.forward_branch(rec)
    rec_perc_loss = 0
    for i in range(len(recF_BE)):
        rec_perc_loss += nn.MSELoss()(recF_BE[i], cF_BE[i].data)
    return (feat_loss, rec_pixl_loss, rec_perc_loss, rec, c)
