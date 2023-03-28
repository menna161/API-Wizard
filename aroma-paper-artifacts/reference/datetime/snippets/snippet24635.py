from datetime import datetime
import os
import re
import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
import matplotlib.pyplot as plt


def plot(self, *, show=True, save=False, settings={}):
    "\n        Plot the airfoil and camber line\n\n        Note:\n            * 'show' and/or 'save' must be True\n\n        Args:\n            :show: (bool) Create an interactive plot\n            :save: (bool) Save plot to file\n            :settings: (bool) Plot settings\n\n        Plot settings:\n            * Plot settings must be a dictionary\n            * Allowed keys:\n\n            'points': (bool) ==> Plot coordinate points\n            'camber': (bool) ==> Plot camber\n            'chord': (bool) ==> Plot chord\n            'path': (str) ==> Output path (directory path, must exists)\n            'file_name': (str) ==> Full file name\n\n        Returns:\n            None or 'file_name' (full path) if 'save' is True\n        "
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([0, 1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal')
    ax.grid()
    ax.plot(self._x_upper, self._y_upper, '-', color='blue')
    ax.plot(self._x_lower, self._y_lower, '-', color='green')
    if settings.get('points', False):
        ax.plot(self.all_points[0, :], self.all_points[1, :], '.', color='grey')
    if settings.get('camber', False):
        x = np.linspace(0, 1, int((POINTS_AIRFOIL / 2)))
        ax.plot(x, self.camber_line(x), '--', color='red')
    if settings.get('chord', False):
        pass
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.98, top=0.98, wspace=None, hspace=None)
    if show:
        plt.show()
    if save:
        path = settings.get('path', '.')
        file_name = settings.get('file_name', False)
        if (not file_name):
            now = datetime.strftime(datetime.now(), format='%F_%H%M%S')
            file_type = 'png'
            file_name = f'airfoils_{now}.{file_type}'
        fig.savefig(os.path.join(path, file_name))
        return file_name
