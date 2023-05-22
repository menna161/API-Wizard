from os import path, makedirs
import numpy as np
from pyshtools.spectralanalysis import Curve2Mask
from sphericalpolygon import create_polygon
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from ..gg.utils import month2int, med, crop_region
from ..gg.lsq import lsqm, ilsqm, wlsqm, iwlsqm
from ..gg.leakage import forward_model, space_domain
from .class_Series import Series


def plot(self, fig_name, ylabel, block=None, polygons=None, circles=None):
    '\n        Plot grids data.\n\n        Usage: plot_figure(region,buffer_edge,lons_region,lats_region,data_region,fig_name,circles)\n\n        INPUTS:\n            region: [float array] range of region, for example, [96.0,120.0,21.0,39.0] means \n            the boundaries;\n            fig_name: [str] filename of the output figure;\n            ylabel: [str] the label of y axis;\n            circles: [float array] the boundary of circles or polygons; if None, no circles\n            will be plotted.\n\n        OUTPUTS:\n            figure: the output figure;\n        '
    if (not ('rate' in self.title)):
        raise Exception('The shape of the grid data to be plotted should be like (1,d1,d2)')
    (lons_region, lats_region) = (self.lons, self.lats)
    grids_region = self.grids
    img_extent = self.region
    (leftlon, rightlon, lowerlat, upperlat) = img_extent
    lon_step = (rightlon - leftlon)
    lat_step = (upperlat - lowerlat)
    buffer_edge = (lons_region[1] - lons_region[0])
    gridlons = np.append((lons_region - (buffer_edge / 2)), (lons_region[(- 1)] + (buffer_edge / 2)))
    gridlats = np.append((lats_region + (buffer_edge / 2)), (lats_region[(- 1)] - (buffer_edge / 2)))
    fig_dir = 'figures/'
    if (not path.exists(fig_dir)):
        makedirs(fig_dir)
    proj = ccrs.PlateCarree(central_longitude=180)
    for grid_region in grids_region:
        plt.clf()
        fig = plt.figure(dpi=200)
        ax = fig.add_subplot(1, 1, 1, projection=proj)
        ax.set_extent(img_extent, crs=ccrs.PlateCarree())
        gl = ax.gridlines(xlocs=np.linspace(leftlon, rightlon, (med(int(lon_step)) + 1)), ylocs=np.linspace(lowerlat, upperlat, (med(int(lat_step)) + 1)), draw_labels=True, linestyle='--', alpha=0.7)
        (gl.xlabels_top, gl.ylabels_right) = (False, False)
        (gl.xformatter, gl.yformatter) = (LONGITUDE_FORMATTER, LATITUDE_FORMATTER)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
        ax.add_feature(cfeature.RIVERS.with_scale('50m'))
        ax.add_feature(cfeature.LAKES.with_scale('50m'))
        (XX, YY) = np.meshgrid(lons_region, lats_region)
        Z = grid_region
        abs_Z_max = np.abs(Z).max()
        Z_levels = np.linspace((- abs_Z_max), abs_Z_max, 101)
        if (block is None):
            CS = ax.contourf(XX, YY, Z, levels=Z_levels, extend='both', cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
        else:
            CS = ax.pcolormesh(gridlons, gridlats, Z, norm=colors.BoundaryNorm(boundaries=Z_levels, ncolors=256), cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
        cbar = plt.colorbar(CS, extend='both', format='%.0f', shrink=0.9)
        cbar.ax.set_ylabel(ylabel, fontsize=8)
        cbar.ax.tick_params(labelsize=8)
        if (polygons is not None):
            ax.plot(polygons[(:, 1)], polygons[(:, 0)], color='m', transform=ccrs.Geodetic())
        if (circles is not None):
            ax.scatter(circles[(:, 1)], circles[(:, 0)], facecolors='None', color='m', s=(buffer_edge * 30), transform=ccrs.Geodetic(), alpha=0.5)
        plt.savefig((fig_dir + fig_name), bbox_inches='tight')
