import numpy as np
from numpy import sqrt
from numpy.testing import assert_array_almost_equal, assert_almost_equal
from sklearn.utils import check_random_state
from modl.utils.math.enet import enet_norm, enet_projection, enet_scale


def enet_projection_slow(v, radius=1, l1_ratio=0.1):
    'Projection on the elastic-net ball\n    **References:**\n\n    J. Mairal, F. Bach, J. Ponce, G. Sapiro, 2009: Online dictionary learning\n    for sparse coding (http://www.di.ens.fr/sierra/pdfs/icml09.pdf)\n    '
    random_state = check_random_state(None)
    if (l1_ratio == 0):
        return (v / sqrt(np.sum((v ** 2))))
    gamma = ((2 / l1_ratio) - 2)
    radius /= l1_ratio
    m = v.shape[0]
    b_abs = np.abs(v)
    norm = _enet_norm_for_projection(b_abs, gamma)
    if (norm <= radius):
        return v
    else:
        s = 0
        rho = 0
        U = np.arange(m)
        mask = np.ones(m, dtype=np.bool)
        mask_non_zero = mask.nonzero()[0]
        while (mask_non_zero.shape[0] != 0):
            k = random_state.randint(mask_non_zero.shape[0])
            idx = mask_non_zero[k]
            k = U[idx]
            sel = (b_abs < b_abs[k])
            G = U[((~ sel) * mask)]
            d_rho = G.shape[0]
            d_s = _enet_norm_for_projection(b_abs[G], gamma)
            if (((s + d_s) - (((rho + d_rho) * (1 + ((gamma / 2) * b_abs[k]))) * b_abs[k])) < (radius * ((1 + (gamma * b_abs[k])) ** 2))):
                s += d_s
                rho += d_rho
                mask *= sel
            else:
                mask *= (~ sel)
                mask[idx] = False
            mask_non_zero = mask.nonzero()[0]
        if (gamma != 0):
            a = (((gamma ** 2) * radius) + ((gamma * rho) * 0.5))
            b_ = (((2 * radius) * gamma) + rho)
            c = (radius - s)
            l = (((- b_) + np.sqrt(((b_ ** 2) - ((4 * a) * c)))) / (2 * a))
        else:
            l = ((s - radius) / rho)
        b_sign = np.sign(v)
        b_sign[(b_sign == 0)] = 1
        return ((b_sign * np.maximum(np.zeros_like(b_abs), (b_abs - l))) / (1 + (l * gamma)))
