import argparse
from glob import glob
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from data_gen import CHAR_IDX
from utils import LogicSeq
from models import build_model
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from mpl_toolkits.mplot3d import Axes3D


def showsave_plot():
    'Show or save plot.'
    if ARGS.outf:
        plt.savefig(ARGS.outf, bbox_inches='tight')
    else:
        plt.show()
