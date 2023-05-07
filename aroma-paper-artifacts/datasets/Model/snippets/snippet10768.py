from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import GPy
import matplotlib.pyplot as plt
import numpy as np
import emukit.multi_fidelity
import emukit.test_functions
from emukit.model_wrappers.gpy_model_wrappers import GPyMultiOutputWrapper
from emukit.multi_fidelity.convert_lists_to_array import convert_x_list_to_array
from emukit.multi_fidelity.convert_lists_to_array import convert_xy_lists_to_arrays
from emukit.multi_fidelity.models import GPyLinearMultiFidelityModel


def train(self, x_l, y_l, x_h, y_h):
    (X_train, Y_train) = convert_xy_lists_to_arrays([x_l, x_h], [y_l, y_h])
    kernels = [GPy.kern.RBF(x_l.shape[1]), GPy.kern.RBF(x_h.shape[1])]
    kernel = emukit.multi_fidelity.kernels.LinearMultiFidelityKernel(kernels)
    gpy_model = GPyLinearMultiFidelityModel(X_train, Y_train, kernel, n_fidelities=2)
    if (self.noise is not None):
        gpy_model.mixed_noise.Gaussian_noise.fix(self.noise)
        gpy_model.mixed_noise.Gaussian_noise_1.fix(self.noise)
    self.model = GPyMultiOutputWrapper(gpy_model, 2, n_optimization_restarts=self.n_optimization_restarts)
    self.model.optimize()
