import os
import subprocess
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time
import warnings


def save_figs(filename=None, open=True, folder='.', save_latest=True):
    '\n\n    :param filename: (optional) path to pdf file for saving.\n    :param open: boolean flag for opening pdf file after saving\n    :param folder: folder to save pdf files (default=current dir)\n    :param save_latest: boolean flag for creating a "latest.pdf" in folder directory, symlinked to latest plots.\n    :return:\n    '
    if (filename is None):
        filename = time.strftime('%Y%m%d-%H%M%S.pdf')
    if (folder is not None):
        if (not os.path.exists(folder)):
            os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, filename)
    fn = os.path.join(os.getcwd(), filename)
    pp = PdfPages(fn)
    for i in plt.get_fignums():
        plt.figure(i).tight_layout()
        pp.savefig(plt.figure(i))
        plt.close(plt.figure(i))
    pp.close()
    if save_latest:
        try:
            latest_path = os.path.join(folder, 'latest.pdf')
            if os.path.exists(latest_path):
                os.remove(latest_path)
            os.symlink(filename, latest_path)
            if open:
                _open_figs(latest_path)
            return
        except OSError:
            warnings.warn('Cannot create symbolic link in Windows without administrator privileges. Skipping.')
    if open:
        _open_figs(filename)
