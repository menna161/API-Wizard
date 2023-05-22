from os import path, makedirs
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def plot_at_northpole(lons, lats, data, fig_name, ylabel=None, magnify=None):
    "\n    Plot grid data at the northpole. Note: The value of the grid data was magnified 1000 times during the plot process. \n\n    Usage:\n    plot_at_northpole(lons,lats,data,fig_name)\n    plot_at_northpole(lons,lats,data,fig_name,1e3)\n\n    Inputs:\n    lons -> [float array] logitudes\n    lats -> [float array] latitudes\n    data -> [float 2d array] grid data\n    fig_name -> [str] figure name\n    ylabel -> [str] ylabel, such as '$10^{-3}$ [mm w.e.]'\n\n    Parameters:\n    magnify -> [optional, float, default = None] If None, 1 is taken.\n    \n    Outputs: A png(200dpi) image stored in the figures directory \n    "
    fig_dir = 'figures/'
    if (not path.exists(fig_dir)):
        makedirs(fig_dir)
    plt.clf()
    fig = plt.figure(dpi=200)
    proj = ccrs.NearsidePerspective(0, 90, 2000000.0)
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    gl = ax.gridlines(xlocs=np.linspace(0, 360, 7), ylocs=np.linspace(90, 0, 10), linestyle='--', alpha=0.7)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.LAKES)
    if (magnify is None):
        magnify = 1
    (XX, YY) = np.meshgrid(lons, lats)
    Z = (data * magnify)
    abs_Z_max = np.abs(Z).max()
    Z_levels = np.linspace((- abs_Z_max), abs_Z_max, 61)
    CS = ax.contourf(XX, YY, Z, levels=Z_levels, extend='both', cmap=plt.cm.RdBu_r, zorder=0, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(CS, extend='both', format='%.0f', shrink=0.9)
    cbar.ax.set_ylabel(ylabel, fontsize=8)
    cbar.ax.tick_params(labelsize=8)
    return plt.savefig(fig_name, bbox_inches='tight')
