import torch
import numpy as np


def __init__(self, N):
    self.args = locals().copy()
    self.args.pop('self')
    self.N = N
    N_m = int((N / 2))
    self.scale = [((2 * np.pi) / N_m)]
    if (self.N == 0):
        h_list = torch.tensor([], dtype=torch.float32)
    else:
        h_list = np.array([np.linspace(0, ((2 * np.pi) - ((2 * np.pi) / N_m)), N_m)], dtype=np.float32).transpose()
        h_list_m = np.stack((np.concatenate((h_list, h_list), axis=0).squeeze(), np.concatenate((np.ones(N_m, dtype=np.float32), ((- 1) * np.ones(N_m, dtype=np.float32)))).transpose()), axis=1)
        h_list_m = torch.from_numpy(h_list_m)
    self.grid = h_list_m
    H.haar_meas = (2 * ((2 * np.pi) / N_m))
