from os import path, makedirs
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import correlate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import GPy
from ..gg.utils import month2int
from ..gg.fit_func import func
from ..gg.lsq import lsqm, ilsqm, wlsqm, iwlsqm


def plot(self, fig_name, ylabel, kernel='mat32+period', mode='ILSQM'):
    "\n        The time series consists of a linear trend, annual variation, and interannual variation. \n        The linear trend and interannual variation together make up the long-term trend. \n        The time series is fitted by the Gaussian Process Regression(GPR) technique. \n        Currently, available kernels for GPR here include 'rbf', 'rbf+period', 'mat32+period', 'mat52+period', 'linear+period', 'spline+period', and 'poly+period'. \n        If the kernel is not specified, it defaults to 'mat32+period'. \n        To extract the long-term trend from the GPR fitted curve, a Gaussian filter with a radius of 3 years is employed.\n        "
    if ('rate' in self.title):
        raise Exception('The shape of the series data to be plotted should contain multiple elements')
    fig_dir = 'figures/'
    if (not path.exists(fig_dir)):
        makedirs(fig_dir)
    (qs, qs_std) = (self.qs, self.qs_std)
    month = month2int(self.solution_month)
    qs_rate = qs_rate_std = 0
    normal = np.ones_like(qs, dtype=bool)
    if (mode is 'LSQM'):
        (qs_rate, qs_rate_std, intercept, _) = lsqm(month, qs)
    elif (mode is 'WLSQM'):
        (qs_rate, qs_rate_std, intercept, _) = wlsqm(month, qs, qs_std)
    elif (mode is 'ILSQM'):
        (qs_rate, qs_rate_std, normal, intercept, _) = ilsqm(month, qs)
    elif (mode is 'IWLSQM'):
        (qs_rate, qs_rate_std, normal, intercept, _) = iwlsqm(month, qs, qs_std)
    else:
        raise Exception('Currently, the least square method can only be LSQM, WLSQM, ILSQM, and IWLSQM.')
    total_month_index = np.arange(self.total_month_counts)
    fit_qs = func(total_month_index, intercept, qs_rate)
    qs_deanomaly = qs[normal]
    month_deanomaly = month[normal]
    if (kernel == 'rbf'):
        kernel = GPy.kern.RBF(input_dim=1)
    elif (kernel == 'rbf+period'):
        kernel = (GPy.kern.RBF(input_dim=1) + GPy.kern.StdPeriodic(input_dim=1, period=12))
    elif (kernel == 'mat32+period'):
        kernel = (GPy.kern.Matern32(input_dim=1) + GPy.kern.StdPeriodic(input_dim=1, period=12))
    elif (kernel == 'mat52+period'):
        kernel = (GPy.kern.Matern32(input_dim=1) + GPy.kern.StdPeriodic(input_dim=1, period=12))
    elif (kernel == 'linear+period'):
        kernel = (GPy.kern.Linear(input_dim=1) + GPy.kern.StdPeriodic(input_dim=1, period=12))
    elif (kernel == 'spline+period'):
        kernel = (GPy.kern.Spline(input_dim=1) + GPy.kern.StdPeriodic(input_dim=1, period=12))
    elif (kernel == 'poly+period'):
        kernel = (GPy.kern.Poly(input_dim=1) + GPy.kern.StdPeriodic(input_dim=1, period=12))
    else:
        raise Exception('Currently, kernels can only be rbf, rbf+period, mat32+period, mat52+period, linear+period, spline+period, and poly+period.')
    model = GPy.models.GPRegression(month_deanomaly[(:, None)], qs_deanomaly[(:, None)], kernel)
    model.optimize()
    (mean, var) = model.predict(total_month_index[(:, None)])
    month_date = np.array(self.total_month, dtype=np.datetime64)
    plt.clf()
    fig = plt.figure(dpi=200)
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.ylabel(ylabel)
    plt.scatter(month_deanomaly, qs_deanomaly, marker='+', s=25, label=None)
    plt.plot(total_month_index, mean[(:, 0)], linewidth=1.5, color='red', label=None)
    plt.plot(total_month_index, fit_qs, linewidth=1.5, linestyle='dashed', color='black', label='Linear Trend')
    plt.plot(total_month_index, gaussian_filter(mean[(:, 0)], 9), linewidth=1.5, color='green', label='Long-term Trend')
    plt.legend(loc='best', fontsize='x-small')
    plt.xticks(total_month_index[::24], month_date[::24])
    plt.setp(ax.get_xticklabels(), rotation=30)
    plt.savefig((fig_dir + fig_name), bbox_inches='tight')
