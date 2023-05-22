import os
import numpy as np
from matplotlib import pyplot as plt


def save(self):
    if (self._test_valid_step() is True):
        fig = plt.figure(figsize=self.figsize)
        plt.plot(self.step[1:], self.value[1:], '-')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, (self.name + self.postfix)), bbox_inches='tight')
        plt.close(fig)
        fig = plt.figure(figsize=self.figsize)
        plt.plot(self.step[1:], self.ma_value[1:], '-')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, ((self.name + '_ma') + self.postfix)), bbox_inches='tight')
        plt.close(fig)
    else:
        fig = plt.figure(figsize=self.figsize)
        plt.plot(self.value[1:], '-')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, (self.name + self.postfix)), bbox_inches='tight')
        plt.close(fig)
        fig = plt.figure(figsize=self.figsize)
        plt.plot(self.ma_value[1:], '-')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, ((self.name + '_ma') + self.postfix)), bbox_inches='tight')
        plt.close(fig)
    np.savez(os.path.join(self.path, (self.name + '.npz')), value=self.value[1:], ma_value=self.ma_value, original_value=self.original_value)
