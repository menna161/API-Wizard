import numpy as np
import astropy.io.fits as pf
from math import *
import cluster
from matplotlib import pylab as pl


def find_shock_in(clstr: cluster.ClusterObj):
    xray = pf.getdata(clstr.combined_signal)
    temp = pf.getdata(clstr.temperature_map_filename)
    thead = pf.getheader(clstr.temperature_map_filename)
    res = pf.getdata(clstr.scale_map_file)
    xray[(temp == 0)] = 0
    res = (1.25 * res)
    nx = temp.shape[0]
    ny = temp.shape[1]
    mach = np.zeros((nx, ny), dtype='d')
    angle = np.zeros((nx, ny), dtype='d')
    i_plus = np.zeros((nx, ny), dtype='i')
    i_minus = np.zeros((nx, ny), dtype='i')
    j_plus = np.zeros((nx, ny), dtype='i')
    j_minus = np.zeros((nx, ny), dtype='i')
    Tjump = np.zeros((nx, ny), dtype='d')
    Xjump = np.zeros((nx, ny), dtype='d')
    max_Tjump = np.ones((nx, ny), dtype='d')
    max_theta = np.zeros((nx, ny), dtype='d')
    Xyes = np.zeros((nx, ny))
    mask = np.ones((nx, ny))
    XT = np.zeros((nx, ny), dtype='d')
    i = np.zeros((nx, ny), dtype='i')
    j = np.zeros((nx, ny), dtype='i')
    for k in range(ny):
        i[(:, k)] = np.arange(nx)
    for k in range(nx):
        j[(k:,)] = np.arange(ny)
    theta = 0.0
    while (theta < np.pi):
        print(theta)
        i_plus = np.rint((i + (res * sin(theta))))
        i_minus = ((i + i) - i_plus)
        j_plus = np.rint((j + (res * cos(theta))))
        j_minus = ((j + j) - j_plus)
        i_plus = i_plus.astype(int)
        i_minus = i_minus.astype(int)
        j_plus = j_plus.astype(int)
        j_minus = j_minus.astype(int)
        i_plus[(i_plus > (nx - 1))] = 0
        i_plus[(i_plus < 0)] = 0
        i_minus[(i_minus > (nx - 1))] = 0
        i_minus[(i_minus < 0)] = 0
        j_plus[(j_plus > (ny - 1))] = 0
        j_plus[(j_plus < 0)] = 0
        j_minus[(j_minus > (ny - 1))] = 0
        j_minus[(j_minus < 0)] = 0
        pix1 = (temp[(i_plus, j_plus)] > 0.0)
        pix2 = (temp[(i_minus, j_minus)] > 0.0)
        pix = (pix1 * pix2)
        print('temp = ', temp[(i_minus[pix], j_minus[pix])])
        print('xray = ', xray[(i_minus[pix], j_minus[pix])])
        Tjump[pix] = (temp[(i_plus[pix], j_plus[pix])] / temp[(i_minus[pix], j_minus[pix])])
        Xjump[pix] = (xray[(i_plus[pix], j_plus[pix])] / xray[(i_minus[pix], j_minus[pix])])
        plus_pix = (Tjump > max_Tjump)
        minus_pix = ((1.0 / Tjump) > max_Tjump)
        max_Tjump[plus_pix] = Tjump[plus_pix]
        max_theta[plus_pix] = theta
        max_Tjump[minus_pix] = (1.0 / Tjump[minus_pix])
        max_theta[minus_pix] = (theta + np.pi)
        XT[plus_pix] = ((np.sign(((Tjump[plus_pix] - 1.0) * (Xjump[plus_pix] - 1.0))) * 0.5) + 0.5)
        XT[minus_pix] = ((np.sign(((Tjump[minus_pix] - 1.0) * (Xjump[minus_pix] - 1.0))) * 0.5) + 0.5)
        theta = (theta + (np.pi / 32.0))
    mach[(XT == 1.0)] = (0.2 * (((- 7.0) + (8.0 * max_Tjump[(XT == 1.0)])) + (4.0 * np.sqrt(((4.0 - (7.0 * max_Tjump[(XT == 1.0)])) + (4.0 * (max_Tjump[(XT == 1.0)] ** 2)))))))
    angle[(XT == 1.0)] = (max_theta[(XT == 1.0)] + (180.0 / np.pi))
    angle[(XT != 1.0)] = (- 1.0)
    mach = np.sqrt(mach)
    angle[np.isnan(mach)] = (- 1.0)
    mach[np.isnan(mach)] = 0.0
    mach[(temp == 0.0)] = np.nan
    angle[(temp == 0.0)] = np.nan
    for ii in range(0, nx):
        for jj in range(0, ny):
            if (mach[(ii, jj)] > 5):
                mach[(ii, jj)] = 0
    pf.writeto(clstr.mach_map_filename, mach, header=thead, overwrite=True)
    pf.writeto(clstr.angle_map_filename, angle, header=thead, overwrite=True)
    (sa2d, mach2d) = pl.histogram(mach, bins=50, range=[0.1, 4.0])
    pl.clf()
    pl.semilogy(mach2d[1:], (sa2d / (mach2d[1] - mach2d[0])), 'k', ls='steps-')
    pl.xlabel('Mach')
    pl.ylabel('pixels')
    pl.xlim(0.1, 4.0)
    pl.ylim(100.0, 1500000.0)
    pl.savefig(clstr.mach_histogram_filename, dpi=200, bbox_inches='tight')
