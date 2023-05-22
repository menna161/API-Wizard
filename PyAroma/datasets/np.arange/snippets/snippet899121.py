from __future__ import print_function
import json
import os
import dataset_setup_constants as ds_constants
import mass_spec_constants as ms_constants
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as PilImage
import six
import tensorflow as tf


def plot_true_and_predicted_spectra(true_dense_spectra, generated_dense_spectra, plot_mode_key=PlotModeKeys.PREDICTED_SPECTRUM, output_filename='', rescale_mz_axis=False):
    'Generates a plot comparing a true and predicted mass spec spectra.\n\n  If output_filename given, saves a png file of the spectra, with the\n  true spectrum above and predicted spectrum below.\n\n  Args:\n    true_dense_spectra : np.array representing the true mass spectra\n    generated_dense_spectra : np.array representing the predicted mass spectra\n    plot_mode_key: a PlotModeKeys instance\n    output_filename : str path for saving generated image.\n    rescale_mz_axis: Setting to rescale m/z axis according to highest m/z peak\n        location.\n\n  Returns:\n    np.array of the bits of the generated matplotlib plot.\n  '
    if (not rescale_mz_axis):
        x_array = np.arange(SPECTRA_PLOT_PEAK_LOC_LIMIT)
        bar_width = SPECTRA_PLOT_BAR_LINE_WIDTH
        mz_max = SPECTRA_PLOT_PEAK_LOC_LIMIT
    else:
        mz_max = max(max(np.nonzero(true_dense_spectra)[0]), max(np.nonzero(generated_dense_spectra)[0]))
        if ((mz_max + SPECTRA_PLOT_MZ_MAX_OFFSET) < ms_constants.MAX_PEAK_LOC):
            mz_max += SPECTRA_PLOT_MZ_MAX_OFFSET
        else:
            mz_max = ms_constants.MAX_PEAK_LOC
        x_array = np.arange(mz_max)
        true_dense_spectra = true_dense_spectra[:mz_max]
        generated_dense_spectra = generated_dense_spectra[:mz_max]
        bar_width = ((SPECTRA_PLOT_BAR_LINE_WIDTH * mz_max) / ms_constants.MAX_PEAK_LOC)
    figure = plt.figure(figsize=SPECTRA_PLOT_FIGURE_SIZE, dpi=300)
    ax_main = figure.add_subplot(111, frameon=False)
    ax_main.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    ax_main.set_xlabel(SPECTRA_PLOT_X_AXIS_LABEL)
    ax_main.set_ylabel(SPECTRA_PLOT_Y_AXIS_LABEL)
    if six.PY2:
        ax_top = figure.add_subplot(211, axisbg=SPECTRA_PLOT_BACKGROUND_COLOR)
    else:
        ax_top = figure.add_subplot(211, facecolor=SPECTRA_PLOT_BACKGROUND_COLOR)
    bar_top = ax_top.bar(x_array, true_dense_spectra, bar_width, color=SPECTRA_PLOT_TRUE_SPECTRA_COLOR, edgecolor=SPECTRA_PLOT_TRUE_SPECTRA_COLOR)
    ax_top.set_ylim((0, SPECTRA_PLOT_INTENSITY_LIMIT))
    plt.setp(ax_top.get_xticklabels(), visible=False)
    ax_top.grid(color=SPECTRA_PLOT_GRID_COLOR, linewidth=SPECTRA_PLOT_BAR_GRID_LINE_WIDTH)
    if six.PY2:
        ax_bottom = figure.add_subplot(212, axisbg=SPECTRA_PLOT_BACKGROUND_COLOR)
    else:
        ax_bottom = figure.add_subplot(212, facecolor=SPECTRA_PLOT_BACKGROUND_COLOR)
    figure.subplots_adjust(hspace=0.0)
    bar_bottom = ax_bottom.bar(x_array, generated_dense_spectra, bar_width, color=SPECTRA_PLOT_PREDICTED_SPECTRA_COLOR, edgecolor=SPECTRA_PLOT_PREDICTED_SPECTRA_COLOR)
    ax_bottom.set_ylim((SPECTRA_PLOT_INTENSITY_LIMIT, 0))
    ax_bottom.set_xlim(0, mz_max)
    yticks_bottom = ax_bottom.yaxis.get_major_ticks()
    yticks_bottom[0].label1.set_visible(False)
    ax_bottom.grid(color=SPECTRA_PLOT_GRID_COLOR, linewidth=SPECTRA_PLOT_BAR_GRID_LINE_WIDTH)
    for ax in [ax_top, ax_bottom]:
        ax.minorticks_on()
        ax.tick_params(axis='y', which='minor', left='off')
        ax.tick_params(axis='y', which='minor', right='off')
    ax_top.tick_params(axis='x', which='minor', top='off')
    if (plot_mode_key == PlotModeKeys.PREDICTED_SPECTRUM):
        ax_top.legend((bar_top, bar_bottom), (SPECTRA_PLOT_ACTUAL_SPECTRA_LEGEND_TEXT, SPECTRA_PLOT_PREDICTED_SPECTRA_LEGEND_TEXT), **SPECTRA_PLOT_PLACE_LEGEND_ABOVE_CHART_KWARGS)
    elif (plot_mode_key == PlotModeKeys.LIBRARY_MATCHED_SPECTRUM):
        ax_top.legend((bar_top, bar_bottom), (SPECTRA_PLOT_QUERY_SPECTRA_LEGEND_TEXT, SPECTRA_PLOT_LIBRARY_MATCH_SPECTRA_LEGEND_TEXT), **SPECTRA_PLOT_PLACE_LEGEND_ABOVE_CHART_KWARGS)
    figure.canvas.draw()
    data = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    try:
        data = np.reshape(data, SPECTRA_PLOT_DIMENSIONS_RGB)
    except ValueError:
        raise ValueError('The shape of the np.array generated from the data does not match the values in SPECTRA_PLOT_DIMENSIONS_RGB : {}'.format(SPECTRA_PLOT_DIMENSIONS_RGB))
    if output_filename:
        if ((not output_filename.endswith('.png')) or output_filename.endswith('.eps')):
            output_filename += '.png'
        with tf.gfile.GFile(output_filename, 'wb') as out:
            image = PilImage.fromarray(data).convert('RGB')
            image.save(out, dpi=(SPECTRA_PLOT_DPI, SPECTRA_PLOT_DPI))
    tf.logging.info('Shape of spectra plot data {} '.format(np.shape(data)))
    plt.close(figure)
    return data
