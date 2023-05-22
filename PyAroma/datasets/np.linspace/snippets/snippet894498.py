import torch
import torch.nn
from torch.autograd import Variable
import numpy as np


def bilinearInterpPointTnf(matches, target_points_norm, feature_size=None):
    (xA, yA, xB, yB) = matches
    if (feature_size is None):
        feature_size = int(np.sqrt(xB.shape[(- 1)]))
    (b, _, N) = target_points_norm.size()
    X_ = xB.view((- 1))
    Y_ = yB.view((- 1))
    grid = torch.FloatTensor(np.linspace((- 1), 1, feature_size)).unsqueeze(0).unsqueeze(2)
    if xB.is_cuda:
        grid = grid.cuda()
    if isinstance(xB, Variable):
        grid = Variable(grid)
    x_minus = (torch.sum(((target_points_norm[(:, 0, :)] - grid) > 0).long(), dim=1, keepdim=True) - 1)
    x_minus[(x_minus < 0)] = 0
    x_plus = (x_minus + 1)
    y_minus = (torch.sum(((target_points_norm[(:, 1, :)] - grid) > 0).long(), dim=1, keepdim=True) - 1)
    y_minus[(y_minus < 0)] = 0
    y_plus = (y_minus + 1)
    toidx = (lambda x, y, L: ((y * L) + x))
    m_m_idx = toidx(x_minus, y_minus, feature_size)
    p_p_idx = toidx(x_plus, y_plus, feature_size)
    p_m_idx = toidx(x_plus, y_minus, feature_size)
    m_p_idx = toidx(x_minus, y_plus, feature_size)
    topoint = (lambda idx, X, Y: torch.cat((X[idx.view((- 1))].view(b, 1, N).contiguous(), Y[idx.view((- 1))].view(b, 1, N).contiguous()), dim=1))
    P_m_m = topoint(m_m_idx, X_, Y_)
    P_p_p = topoint(p_p_idx, X_, Y_)
    P_p_m = topoint(p_m_idx, X_, Y_)
    P_m_p = topoint(m_p_idx, X_, Y_)
    multrows = (lambda x: (x[(:, 0, :)] * x[(:, 1, :)]))
    f_p_p = multrows(torch.abs((target_points_norm - P_m_m)))
    f_m_m = multrows(torch.abs((target_points_norm - P_p_p)))
    f_m_p = multrows(torch.abs((target_points_norm - P_p_m)))
    f_p_m = multrows(torch.abs((target_points_norm - P_m_p)))
    Q_m_m = topoint(m_m_idx, xA.view((- 1)), yA.view((- 1)))
    Q_p_p = topoint(p_p_idx, xA.view((- 1)), yA.view((- 1)))
    Q_p_m = topoint(p_m_idx, xA.view((- 1)), yA.view((- 1)))
    Q_m_p = topoint(m_p_idx, xA.view((- 1)), yA.view((- 1)))
    warped_points_norm = (((((Q_m_m * f_m_m) + (Q_p_p * f_p_p)) + (Q_m_p * f_m_p)) + (Q_p_m * f_p_m)) / (((f_p_p + f_m_m) + f_m_p) + f_p_m))
    return warped_points_norm
