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


def main():
    high_fidelity = emukit.test_functions.forrester.forrester
    low_fidelity = emukit.test_functions.forrester.forrester_low
    x_plot = np.linspace(0, 1, 200)[(:, None)]
    y_plot_l = low_fidelity(x_plot)
    y_plot_h = high_fidelity(x_plot)
    x_train_l = np.atleast_2d(np.random.rand(20)).T
    x_train_h = np.atleast_2d(np.random.permutation(x_train_l)[:8])
    y_train_l = low_fidelity(x_train_l)
    y_train_h = high_fidelity(x_train_h)
    model = LinearMFGP(noise=0, n_optimization_restarts=10)
    model.train(x_train_l, y_train_l, x_train_h, y_train_h)
    (lf_mean, lf_std, hf_mean, hf_std) = model.predict(x_plot)
    plt.figure(figsize=(12, 8))
    plt.plot(x_plot, y_plot_l, 'b')
    plt.plot(x_plot, y_plot_h, 'r')
    plt.scatter(x_train_l, y_train_l, color='b', s=40)
    plt.scatter(x_train_h, y_train_h, color='r', s=40)
    plt.ylabel('f (x)')
    plt.xlabel('x')
    plt.legend(['Low fidelity', 'High fidelity'])
    plt.title('High and low fidelity Forrester functions')
    plt.figure(figsize=(12, 8))
    plt.fill_between(x_plot.flatten(), (lf_mean - (1.96 * lf_std)).flatten(), (lf_mean + (1.96 * lf_std)).flatten(), facecolor='g', alpha=0.3)
    plt.fill_between(x_plot.flatten(), (hf_mean - (1.96 * hf_std)).flatten(), (hf_mean + (1.96 * hf_std)).flatten(), facecolor='y', alpha=0.3)
    plt.plot(x_plot, y_plot_l, 'b')
    plt.plot(x_plot, y_plot_h, 'r')
    plt.plot(x_plot, lf_mean, '--', color='g')
    plt.plot(x_plot, hf_mean, '--', color='y')
    plt.scatter(x_train_l, y_train_l, color='b', s=40)
    plt.scatter(x_train_h, y_train_h, color='r', s=40)
    plt.ylabel('f (x)')
    plt.xlabel('x')
    plt.legend(['Low Fidelity', 'High Fidelity', 'Predicted Low Fidelity', 'Predicted High Fidelity'])
    plt.title('Linear multi-fidelity model fit to low and high fidelity Forrester function')
    plt.show()
