import numpy as np
import torch
import DominantSparseEigenAD.symeig as symeig
import matplotlib.pyplot as plt
import time


def plot(self, target):
    plt.cla()
    plt.plot(self.xmesh, target, label='target')
    plt.plot(self.xmesh, self.psi0.detach().abs().numpy(), label='$\\psi_0$ corresponding to current potential $V$')
    plt.plot(self.xmesh, (self.potential.detach().numpy() / 20000), label='$V$')
    plt.xlabel('$x$')
    plt.legend()
    plt.draw()
