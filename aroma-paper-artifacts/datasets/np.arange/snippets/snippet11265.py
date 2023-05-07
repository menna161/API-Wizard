import numpy as np
import random


def bam_simul_perturb(X, t, param=[0.01, 0.01], name='poisson', ns=1000, resize=0):
    t = t[:]
    if (np.mean(np.diff(t)) > 0):
        isflipped = 1
        X = np.flipud(X)
        t = np.flipud(t)
    else:
        isflipped = 0
        X = X.T
        X = X.T
    (n, p) = np.shape(X)
    if (len(param) == 1):
        param[1] = param[0]
    if (not ('tm' in locals())):
        tm = np.ones((n, p, ns))
        if (name.lower() == 'poisson'.lower()):
            for nn in range(ns):
                num_event_mis = np.random.poisson((param[0] * n), size=(p, 1))
                num_event_dbl = np.random.poisson((param[1] * n), size=(p, 1))
                for ii in range(p):
                    jumps = (np.random.choice((n - 1), num_event_mis[ii][0]) + 1)
                    tm[(jumps, ii, nn)] = (tm[(jumps, ii, nn)] - 1)
                    jumps = (np.random.choice((n - 1), num_event_dbl[ii][0]) + 1)
                    tm[(jumps, ii, nn)] = (tm[(jumps, ii, nn)] + 1)
        elif (name.lower() == 'bernoulli'.lower()):
            for nn in range(ns):
                tm = (tm - np.random.binomial(1, param[0], size=(n, p)))
                tm = (tm + np.random.binomial(1, param[1], size=(n, p)))
        else:
            print('Unknown age model ; acceptable inputs are poisson and bernoulli')
    if (resize == 1):
        t_ext = np.ceil(((2 * param(2)) * n))
        tn = (n + t_ext)
        X = np.concatenate(X, np.nan(t_ext, p))
        dt = (t(2) - t(1))
        time_ext = ((t[(- 1)] + np.arange(dt, t[(- 1)], dt)) + (t_ext * dt.T))
        tp = np.concatenate(t, time_ext.T)
    else:
        tn = n
        tp = t
    Xp = np.empty([tn, p, ns])
    for i in range(tn):
        for j in range(p):
            for k in range(ns):
                Xp[(i, j, k)] = np.nan
    Tmax = 0
    Tmin = n
    tmc = np.ones((tn, p, ns))
    for nn in range(ns):
        for ii in range(p):
            xcount = 0
            Xcount = 0
            tt = 0
            while (tt < n):
                if (tm[(tt, ii, nn)] == 0):
                    Xcount = min((Xcount + 1), tn)
                    tmc[((xcount - 1), ii, nn)] = (tmc[((xcount - 1), ii, nn)] + 1)
                elif (tm[(tt, ii, nn)] == 2):
                    Xp[((xcount - 1), ii, nn)] = X[((Xcount - 1), ii)]
                    tmc[((xcount - 1), ii, nn)] = (tmc[((xcount - 1), ii, nn)] - 1)
                    xcount = min(tn, (xcount + 1))
                Xp[((xcount - 1), ii, nn)] = X[((Xcount - 1), ii)]
                xcount = min(tn, (xcount + 1))
                Xcount = min(tn, (Xcount + 1))
                tt = (tt + 1)
            k = np.where((~ np.isnan(Xp[(:, ii, nn)])))[0][(- 1)]
            if (k > Tmax):
                Tmax = k
            if (k < Tmin):
                Tmin = k
    if (resize == (- 1)):
        Xp = Xp[(1:Tmin, :, :)]
        tp = tp[1:Tmin]
    if (resize == 1):
        Xp = Xp[(1:Tmax, :, :)]
        tp = tp[1:Tmax]
    if (X.shape[1] == 1):
        Xp = np.reshape(Xp, (n, ns))
        tmc = np.reshape(tmc, (n, ns))
    if (isflipped == 1):
        if (X.shape[1] == 1):
            Xp = np.flipud(Xp)
        else:
            for nn in range(ns):
                Xp[(:, :, nn)] = np.flipud(Xp[(:, :, nn)])
                tmc[(:, :, nn)] = np.flipud(tmc[(:, :, nn)])
        tp = np.flipud(tp)
    return (tp, Xp, tmc)
