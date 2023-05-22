import torch.nn as nn
from model import model_original
from model import model_cd


def forward(self, c, iter):
    rec = self.SD(self.SE(c))
    rec_pixl_loss = nn.MSELoss()(rec, c.data)
    recF_BE = self.BE.forward_branch(rec)
    cF_BE = self.BE.forward_branch(c)
    rec_perc_loss = 0
    for i in range(len(recF_BE)):
        rec_perc_loss += nn.MSELoss()(recF_BE[i], cF_BE[i].data)
    return (rec_pixl_loss, rec_perc_loss, rec)
