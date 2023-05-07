import numpy as np


def filterSH(W, cilm, cilm_std=None):
    '\n    Filter spherical harmonic coefficients with a block diagonal fitler matrix.\n\n    Usage:\n    cilm_filter = filterSH(W,cilm)\n    cilm_filter,cilm_std_filter = filterSH(W,cilm,cilm_std)\n\n    Inputs:\n    W -> [dic]: Dictionary containing the filter matrix (read by read_BIN.py)\n    cilm -> [float 3d array] Spherical harmonic coefficients in matrix form. cilm = clm for i = 0; cilm = slm for i = 1\n\n    Parameters:\n    cilm_std -> [float 3d array] standard deviation for the spherical harmonic coefficients\n\n    Outputs:\n    cilm_filter -> [float 3d array] Filtered spherical harmonic coefficients\n    cilm_std_filter -> [float 3d array] standard deviation for the filtered spherical harmonic coefficients\n\n    Notice: \n    This program is translated from the matlab/octave source code filterSH.m written by Roelof Rietbroek 2016. \n    For more information, please refer to https://github.com/strawpants/GRACE-filter\n    '
    lmax = (cilm.shape[1] - 1)
    (lmaxfilt, lminfilt) = (W['Lmax'], W['Lmin'])
    lmaxout = min(lmax, lmaxfilt)
    cilm_filter = np.zeros_like(cilm)
    cilm_std_filter = np.zeros_like(cilm_std)
    (lastblckind, lastindex) = (0, 0)
    for iblk in range(W['Nblocks']):
        degree = ((iblk + 1) // 2)
        if (degree > lmaxout):
            break
        trig = (((iblk + int((iblk > 0))) + 1) % 2)
        sz = (W['blockind'][iblk] - lastblckind)
        blockn = np.identity(((lmaxfilt + 1) - degree))
        lminblk = max(lminfilt, degree)
        shift = (lminblk - degree)
        blockn[(shift:, shift:)] = W['pack1'][lastindex:(lastindex + (sz ** 2))].reshape(sz, sz).T
        if trig:
            cilm_filter[(0, degree:(lmaxout + 1), degree)] = np.dot(blockn[(:((lmaxout + 1) - degree), :((lmaxout + 1) - degree))], cilm[(0, degree:(lmaxout + 1), degree)])
        else:
            cilm_filter[(1, degree:(lmaxout + 1), degree)] = np.dot(blockn[(:((lmaxout + 1) - degree), :((lmaxout + 1) - degree))], cilm[(1, degree:(lmaxout + 1), degree)])
        if (cilm_std is not None):
            if trig:
                cilm_std_filter[(0, degree:(lmaxout + 1), degree)] = np.sqrt(np.dot((blockn[(:((lmaxout + 1) - degree), :((lmaxout + 1) - degree))] ** 2), (cilm_std[(0, degree:(lmaxout + 1), degree)] ** 2)))
            else:
                cilm_std_filter[(1, degree:(lmaxout + 1), degree)] = np.sqrt(np.dot((blockn[(:((lmaxout + 1) - degree), :((lmaxout + 1) - degree))] ** 2), (cilm_std[(1, degree:(lmaxout + 1), degree)] ** 2)))
        lastblckind = W['blockind'][iblk]
        lastindex = (lastindex + (sz ** 2))
    if (cilm_std is None):
        return cilm_filter
    else:
        return (cilm_filter, cilm_std_filter)
