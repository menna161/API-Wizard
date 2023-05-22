import torch
import torch.nn
from torch.autograd import Variable
import numpy as np


def corr_to_matches(corr4d, delta4d=None, k_size=1, do_softmax=False, scale='centered', return_indices=False, invert_matching_direction=False):
    to_cuda = (lambda x: (x.cuda() if corr4d.is_cuda else x))
    (batch_size, ch, fs1, fs2, fs3, fs4) = corr4d.size()
    if (scale == 'centered'):
        (XA, YA) = np.meshgrid(np.linspace((- 1), 1, (fs2 * k_size)), np.linspace((- 1), 1, (fs1 * k_size)))
        (XB, YB) = np.meshgrid(np.linspace((- 1), 1, (fs4 * k_size)), np.linspace((- 1), 1, (fs3 * k_size)))
    elif (scale == 'positive'):
        (XA, YA) = np.meshgrid(np.linspace(0, 1, (fs2 * k_size)), np.linspace(0, 1, (fs1 * k_size)))
        (XB, YB) = np.meshgrid(np.linspace(0, 1, (fs4 * k_size)), np.linspace(0, 1, (fs3 * k_size)))
    (JA, IA) = np.meshgrid(range(fs2), range(fs1))
    (JB, IB) = np.meshgrid(range(fs4), range(fs3))
    (XA, YA) = (Variable(to_cuda(torch.FloatTensor(XA))), Variable(to_cuda(torch.FloatTensor(YA))))
    (XB, YB) = (Variable(to_cuda(torch.FloatTensor(XB))), Variable(to_cuda(torch.FloatTensor(YB))))
    (JA, IA) = (Variable(to_cuda(torch.LongTensor(JA).view(1, (- 1)))), Variable(to_cuda(torch.LongTensor(IA).view(1, (- 1)))))
    (JB, IB) = (Variable(to_cuda(torch.LongTensor(JB).view(1, (- 1)))), Variable(to_cuda(torch.LongTensor(IB).view(1, (- 1)))))
    if invert_matching_direction:
        nc_A_Bvec = corr4d.view(batch_size, fs1, fs2, (fs3 * fs4))
        if do_softmax:
            nc_A_Bvec = torch.nn.functional.softmax(nc_A_Bvec, dim=3)
        (match_A_vals, idx_A_Bvec) = torch.max(nc_A_Bvec, dim=3)
        score = match_A_vals.view(batch_size, (- 1))
        iB = IB.view((- 1))[idx_A_Bvec.view((- 1))].view(batch_size, (- 1))
        jB = JB.view((- 1))[idx_A_Bvec.view((- 1))].view(batch_size, (- 1))
        iA = IA.expand_as(iB)
        jA = JA.expand_as(jB)
    else:
        nc_B_Avec = corr4d.view(batch_size, (fs1 * fs2), fs3, fs4)
        if do_softmax:
            nc_B_Avec = torch.nn.functional.softmax(nc_B_Avec, dim=1)
        (match_B_vals, idx_B_Avec) = torch.max(nc_B_Avec, dim=1)
        score = match_B_vals.view(batch_size, (- 1))
        iA = IA.view((- 1))[idx_B_Avec.view((- 1))].view(batch_size, (- 1))
        jA = JA.view((- 1))[idx_B_Avec.view((- 1))].view(batch_size, (- 1))
        iB = IB.expand_as(iA)
        jB = JB.expand_as(jA)
    if (delta4d is not None):
        (delta_iA, delta_jA, delta_iB, delta_jB) = delta4d
        diA = delta_iA.squeeze(0).squeeze(0)[(iA.view((- 1)), jA.view((- 1)), iB.view((- 1)), jB.view((- 1)))]
        djA = delta_jA.squeeze(0).squeeze(0)[(iA.view((- 1)), jA.view((- 1)), iB.view((- 1)), jB.view((- 1)))]
        diB = delta_iB.squeeze(0).squeeze(0)[(iA.view((- 1)), jA.view((- 1)), iB.view((- 1)), jB.view((- 1)))]
        djB = delta_jB.squeeze(0).squeeze(0)[(iA.view((- 1)), jA.view((- 1)), iB.view((- 1)), jB.view((- 1)))]
        iA = ((iA * k_size) + diA.expand_as(iA))
        jA = ((jA * k_size) + djA.expand_as(jA))
        iB = ((iB * k_size) + diB.expand_as(iB))
        jB = ((jB * k_size) + djB.expand_as(jB))
    xA = XA[(iA.view((- 1)), jA.view((- 1)))].view(batch_size, (- 1))
    yA = YA[(iA.view((- 1)), jA.view((- 1)))].view(batch_size, (- 1))
    xB = XB[(iB.view((- 1)), jB.view((- 1)))].view(batch_size, (- 1))
    yB = YB[(iB.view((- 1)), jB.view((- 1)))].view(batch_size, (- 1))
    if return_indices:
        return (xA, yA, xB, yB, score, iA, jA, iB, jB)
    else:
        return (xA, yA, xB, yB, score)
