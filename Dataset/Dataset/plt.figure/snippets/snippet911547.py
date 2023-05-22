import glob
import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import argparse
import warnings
from pymatgen.io.vasp import Vasprun
from pymatgen.io.vasp.outputs import UnconvergedVASPWarning
import matplotlib
import matplotlib.pyplot as plt
from vasppy.poscar import Poscar
from vasppy.summary import find_vasp_calculations
from vasppy.utils import match_filename


def make_plot(df, fit_params):
    v_min = (df.volume.min() * 0.99)
    v_max = (df.volume.max() * 1.01)
    v_fitting = np.linspace(v_min, v_max, num=50)
    e_fitting = murnaghan(v_fitting, *fit_params)
    plt.figure(figsize=(8.0, 6.0))
    loc = df.converged
    plt.plot(df[loc].volume, df[loc].energy, 'o')
    loc = [(not b) for b in df.converged]
    plt.plot(df[loc].volume, df[loc].energy, 'o', c='grey')
    plt.plot(v_fitting, e_fitting, '--')
    plt.xlabel('volume [$\\mathrm{\\AA}^3$]')
    plt.ylabel('energy [eV]')
    plt.tight_layout()
    plt.savefig('murn.pdf')
