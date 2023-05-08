import os
import numpy as np
import matplotlib.pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
import fsps


def prettify(fig, ax, label=None):
    ax.set_xlim(900.0, 1000000.0)
    ax.set_xscale('log')
    ax.set_ylim(0.01, 2)
    ax.set_xlabel('rest-frame $\\lambda$ ($\\AA$)', fontsize=20)
    ax.set_ylabel('$\\lambda \\, f_\\lambda$', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=16)
    if (label is not None):
        ax.text(0.63, 0.85, label, transform=ax.transAxes, fontsize=16)
    fig.tight_layout()
    return (fig, ax)
