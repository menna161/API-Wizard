import collections
import sys
import os
import os.path
import platform
import re
import six
import subprocess
import time
import warnings
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import openpyxl
import zipfile
import FlowCal.io
import FlowCal.plot
import FlowCal.gate
import FlowCal.transform
import FlowCal.stats
import FlowCal.mef
from Tkinter import Tk
from tkFileDialog import askopenfilename
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas.io.formats.excel as format_module


def process_beads_table(beads_table, instruments_table, base_dir='.', verbose=False, plot=False, plot_dir=None, full_output=False, get_transform_fxn_kwargs={}):
    '\n    Process calibration bead samples, as specified by an input table.\n\n    This function processes the entries in `beads_table`. For each row, the\n    function does the following:\n        - Load the FCS file specified in the field "File Path".\n        - Transform the forward scatter/side scatter and fluorescence\n          channels to RFI\n        - Remove the 250 first and 100 last events.\n        - Remove saturated events in the forward scatter and side scatter\n          channels.\n        - Apply density gating on the forward scatter/side scatter\n          channels.\n        - Generate a standard curve transformation function, for each\n          fluorescence channel in which the associated MEF values are\n          specified.\n        - Generate forward/side scatter density plots and fluorescence\n          histograms, and plots of the clustering and fitting steps of\n          standard curve generation, if `plot` = True.\n\n    Names of forward/side scatter and fluorescence channels are taken from\n    `instruments_table`.\n\n    Parameters\n    ----------\n    beads_table : DataFrame\n        Table specifying beads samples to be processed. For more\n        information about the fields required in this table, please consult\n        the module\'s documentation.\n    instruments_table : DataFrame\n        Table specifying instruments. For more information about the fields\n        required in this table, please consult the module\'s documentation.\n    base_dir : str, optional\n        Directory from where all the other paths are specified.\n    verbose : bool, optional\n        Whether to print information messages during the execution of this\n        function.\n    plot : bool, optional\n        Whether to generate and save density/histogram plots of each\n        sample, and each beads sample.\n    plot_dir : str, optional\n        Directory relative to `base_dir` into which plots are saved. If\n        `plot` is False, this parameter is ignored. If ``plot==True`` and\n        ``plot_dir is None``, plot without saving.\n    full_output : bool, optional\n        Flag indicating whether to include an additional output, containing\n        intermediate results from the generation of the MEF transformation\n        functions.\n    get_transform_fxn_kwargs : dict, optional\n        Additional parameters passed directly to internal\n        ``mef.get_transform_fxn()`` function call.\n\n    Returns\n    -------\n    beads_samples : OrderedDict\n        Processed, gated, and transformed samples, indexed by\n        ``beads_table.index``.\n    mef_transform_fxns : OrderedDict\n        MEF transformation functions, indexed by ``beads_table.index``.\n    mef_outputs : OrderedDict, only if ``full_output==True``\n        Intermediate results from the generation of the MEF transformation\n        functions. For every entry in `beads_table`,\n        :func:`FlowCal.mef.get_transform_fxn()` is called on the\n        corresponding processed and gated beads sample with\n        ``full_output=True``, and the full output (a `MEFOutput`\n        ``namedtuple``) is added to `mef_outputs`. `mef_outputs` is indexed\n        by ``beads_table.index``. Refer to the documentation for\n        :func:`FlowCal.mef.get_transform_fxn()` for more information.\n\n    '
    beads_samples = collections.OrderedDict()
    mef_transform_fxns = collections.OrderedDict()
    mef_outputs = collections.OrderedDict()
    if beads_table.empty:
        if full_output:
            return (beads_samples, mef_transform_fxns, mef_outputs)
        else:
            return (beads_samples, mef_transform_fxns)
    if verbose:
        msg = 'Processing Beads table ({} entries)'.format(len(beads_table))
        print('')
        print(msg)
        print(('=' * len(msg)))
    if (plot and (plot_dir is not None) and (not os.path.exists(os.path.join(base_dir, plot_dir)))):
        os.makedirs(os.path.join(base_dir, plot_dir))
    headers = list(beads_table.columns)
    mef_headers_all = [h for h in headers if re_mef_values.match(h)]
    mef_channels_all = [re_mef_values.match(h).group(1) for h in mef_headers_all]
    for (beads_id, beads_row) in beads_table.iterrows():
        try:
            instruments_row = instruments_table.loc[beads_row['Instrument ID']]
            sc_channels = [instruments_row['Forward Scatter Channel'], instruments_row['Side Scatter Channel']]
            fl_channels = instruments_row['Fluorescence Channels'].split(',')
            fl_channels = [s.strip() for s in fl_channels]
            if verbose:
                print('\nBeads ID {}...'.format(beads_id))
                print('Loading file "{}"...'.format(beads_row['File Path']))
            filename = os.path.join(base_dir, beads_row['File Path'])
            try:
                beads_sample = FlowCal.io.FCSData(filename)
            except IOError:
                raise ExcelUIException('file "{}" not found'.format(beads_row['File Path']))
            if (beads_sample.shape[0] < 400):
                raise ExcelUIException('number of events is lower than 400')
            if verbose:
                print('Performing data transformation...')
            beads_sample = FlowCal.transform.to_rfi(beads_sample, (sc_channels + fl_channels))
            cluster_channels = beads_row['Clustering Channels'].split(',')
            cluster_channels = [cc.strip() for cc in cluster_channels]
            if verbose:
                print('Performing gating...')
            beads_sample_gated = FlowCal.gate.start_end(beads_sample, num_start=250, num_end=100)
            if (beads_sample_gated.data_type == 'I'):
                beads_sample_gated = FlowCal.gate.high_low(beads_sample_gated, channels=sc_channels)
            try:
                density_gate_output = FlowCal.gate.density2d(data=beads_sample_gated, channels=sc_channels, gate_fraction=beads_row['Gate Fraction'], xscale='logicle', yscale='logicle', sigma=5.0, full_output=True)
                beads_sample_gated = density_gate_output.gated_data
                gate_contour = density_gate_output.contour
            except ValueError as ve:
                raise ExcelUIException(ve.message)
            if plot:
                if verbose:
                    print('Plotting density plot and histogram...')
                density_params = {}
                density_params['mode'] = 'scatter'
                density_params['title'] = '{} ({:.1f}% retained)'.format(beads_id, ((beads_sample_gated.shape[0] * 100.0) / beads_sample.shape[0]))
                density_params['xscale'] = 'logicle'
                density_params['yscale'] = 'logicle'
                density_params['xlim'] = ((np.percentile(beads_sample_gated[(:, sc_channels[0])], 5) / (10 ** 0.75)), (np.percentile(beads_sample_gated[(:, sc_channels[0])], 95) * (10 ** 0.75)))
                density_params['ylim'] = ((np.percentile(beads_sample_gated[(:, sc_channels[1])], 5) / (10 ** 0.75)), (np.percentile(beads_sample_gated[(:, sc_channels[1])], 95) * (10 ** 0.75)))
                density_params['sigma'] = 5.0
                hist_params = {'xscale': 'logicle'}
                if (plot_dir is not None):
                    figname = os.path.join(base_dir, plot_dir, 'density_hist_{}.png'.format(beads_id))
                else:
                    figname = None
                plt.figure(figsize=(6, 4))
                FlowCal.plot.density_and_hist(beads_sample, beads_sample_gated, density_channels=sc_channels, hist_channels=cluster_channels, gate_contour=gate_contour, density_params=density_params, hist_params=hist_params, savefig=figname)
            mef_values = []
            mef_channels = []
            for fl_channel in fl_channels:
                if (fl_channel in mef_channels_all):
                    mef_header = mef_headers_all[mef_channels_all.index(fl_channel)]
                    mef_str = beads_row[mef_header]
                    if pd.isnull(mef_str):
                        continue
                    mef_channels.append(fl_channel)
                    mef = mef_str.split(',')
                    mef = [(int(e) if e.strip().isdigit() else np.nan) for e in mef]
                    mef_values.append(mef)
            if mef_values:
                if (not np.all([(len(mef_values_channel) == len(mef_values[0])) for mef_values_channel in mef_values])):
                    raise ExcelUIException((((('Must specify the same number of' + ' MEF Values for each channel.') + " Use 'None' to instruct FlowCal") + ' to ignore a detected') + ' subpopulation.'))
            mef_values = np.array(mef_values)
            if mef_channels:
                if verbose:
                    if (len(mef_channels) == 1):
                        print('Calculating standard curve for channel {}...'.format(mef_channels[0]))
                    else:
                        print('Calculating standard curve for channels {}...'.format(', '.join(mef_channels)))
                mef_output = FlowCal.mef.get_transform_fxn(beads_sample_gated, mef_values, mef_channels=mef_channels, clustering_channels=cluster_channels, verbose=False, plot=plot, plot_filename=beads_id, plot_dir=(os.path.join(base_dir, plot_dir) if (plot_dir is not None) else None), full_output=full_output, **get_transform_fxn_kwargs)
                if full_output:
                    mef_transform_fxn = mef_output.transform_fxn
                else:
                    mef_transform_fxn = mef_output
            else:
                mef_transform_fxn = None
                mef_output = None
        except ExcelUIException as e:
            if verbose:
                print('ERROR: {}'.format(str(e)))
            beads_samples[beads_id] = e
            mef_transform_fxns[beads_id] = None
            if full_output:
                mef_outputs[beads_id] = None
        else:
            beads_samples[beads_id] = beads_sample_gated
            mef_transform_fxns[beads_id] = mef_transform_fxn
            if full_output:
                mef_outputs[beads_id] = mef_output
    if full_output:
        return (beads_samples, mef_transform_fxns, mef_outputs)
    else:
        return (beads_samples, mef_transform_fxns)
