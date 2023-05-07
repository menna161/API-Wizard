import pandas as pd, numpy as np
from dataclasses import dataclass, replace
from axcell.models.linking.metrics import CM
from matplotlib import pyplot as plt
import matplotlib.tri as tri


def plot(self):
    plt.figure(figsize=(6, 6))
    plt.plot(self.results['precision'], self.results['recall'], '.')
    plt.xlabel('precision')
    plt.ylabel('recall')
