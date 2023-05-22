import os
import os.path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import FlowCal

if (__name__ == '__main__'):
    if (not os.path.exists(beads_plot_dir)):
        os.makedirs(beads_plot_dir)
    if (not os.path.exists(samples_plot_dir)):
        os.makedirs(samples_plot_dir)
    print('\nProcessing calibration beads...')
    print('Loading file "{}"...'.format(beads_filename))
    beads_sample = FlowCal.io.FCSData(beads_filename)
    min_beads_sample = FlowCal.io.FCSData(min_beads_filename)
    max_beads_sample = FlowCal.io.FCSData(max_beads_filename)
    print('Performing data transformation...')
    beads_sample = FlowCal.transform.to_rfi(beads_sample)
    min_beads_sample = FlowCal.transform.to_rfi(min_beads_sample)
    max_beads_sample = FlowCal.transform.to_rfi(max_beads_sample)
    print('Performing gating...')
    beads_sample_gated = FlowCal.gate.start_end(beads_sample, num_start=250, num_end=100)
    min_beads_sample_gated = FlowCal.gate.start_end(min_beads_sample, num_start=250, num_end=100)
    max_beads_sample_gated = FlowCal.gate.start_end(max_beads_sample, num_start=250, num_end=100)
    beads_sample_gated = FlowCal.gate.high_low(beads_sample_gated, channels=['FSC', 'SSC'])
    min_beads_sample_gated = FlowCal.gate.high_low(min_beads_sample_gated, channels=['FSC', 'SSC'])
    max_beads_sample_gated = FlowCal.gate.high_low(max_beads_sample_gated, channels=['FSC', 'SSC'])
    density_gate_output = FlowCal.gate.density2d(data=beads_sample_gated, channels=['FSC', 'SSC'], gate_fraction=0.85, sigma=5.0, full_output=True)
    beads_sample_gated = density_gate_output.gated_data
    gate_contour = density_gate_output.contour
    min_density_gate_output = FlowCal.gate.density2d(data=min_beads_sample_gated, channels=['FSC', 'SSC'], gate_fraction=0.85, sigma=5.0, full_output=True)
    min_beads_sample_gated = min_density_gate_output.gated_data
    min_gate_contour = min_density_gate_output.contour
    max_density_gate_output = FlowCal.gate.density2d(data=max_beads_sample_gated, channels=['FSC', 'SSC'], gate_fraction=0.85, sigma=5.0, full_output=True)
    max_beads_sample_gated = max_density_gate_output.gated_data
    max_gate_contour = max_density_gate_output.contour
    print('Plotting density plot and histogram...')
    density_params = {}
    density_params['mode'] = 'scatter'
    density_params['xlim'] = [90, 1023]
    density_params['ylim'] = [90, 1023]
    density_params['sigma'] = 5.0
    plot_filename = '{}/density_hist_{}.png'.format(beads_plot_dir, 'beads')
    min_plot_filename = '{}/min_density_hist_{}.png'.format(beads_plot_dir, 'beads')
    max_plot_filename = '{}/max_density_hist_{}.png'.format(beads_plot_dir, 'beads')
    FlowCal.plot.density_and_hist(beads_sample, beads_sample_gated, density_channels=['FSC', 'SSC'], hist_channels=['FL1', 'FL3'], gate_contour=gate_contour, density_params=density_params, savefig=plot_filename)
    FlowCal.plot.density_and_hist(min_beads_sample, min_beads_sample_gated, density_channels=['FSC', 'SSC'], hist_channels=['FL1', 'FL3'], gate_contour=min_gate_contour, density_params=density_params, savefig=min_plot_filename)
    FlowCal.plot.density_and_hist(max_beads_sample, max_beads_sample_gated, density_channels=['FSC', 'SSC'], hist_channels=['FL1', 'FL3'], gate_contour=max_gate_contour, density_params=density_params, savefig=max_plot_filename)
    print('\nCalculating standard curve for channel FL1...')
    mef_transform_fxn = FlowCal.mef.get_transform_fxn(beads_sample_gated, mef_channels='FL1', mef_values=mefl_values, clustering_channels=['FL1', 'FL3'], verbose=True, plot=True, plot_dir=beads_plot_dir, plot_filename='beads')
    min_mef_transform_fxn = FlowCal.mef.get_transform_fxn(min_beads_sample_gated, mef_channels='FL1', mef_values=min_mefl_values, clustering_channels=['FL1', 'FL3'], verbose=True, plot=True, plot_dir=beads_plot_dir, plot_filename='min_beads')
    max_mef_transform_fxn = FlowCal.mef.get_transform_fxn(max_beads_sample_gated, mef_channels='FL1', mef_values=max_mefl_values, clustering_channels=['FL1', 'FL3'], verbose=True, plot=True, plot_dir=beads_plot_dir, plot_filename='max_beads')
    print('\nProcessing cell samples...')
    samples = []
    for (sample_id, sample_filename) in enumerate(samples_filenames):
        print('\nLoading file "{}"...'.format(sample_filename))
        sample = FlowCal.io.FCSData(sample_filename)
        print('Performing data transformation...')
        sample = FlowCal.transform.to_rfi(sample)
        sample = mef_transform_fxn(sample, channels=['FL1'])
        print('Performing gating...')
        sample_gated = FlowCal.gate.start_end(sample, num_start=250, num_end=100)
        sample_gated = FlowCal.gate.high_low(sample_gated, channels=['FSC', 'SSC', 'FL1'])
        density_gate_output = FlowCal.gate.density2d(data=sample_gated, channels=['FSC', 'SSC'], gate_fraction=0.85, full_output=True)
        sample_gated = density_gate_output.gated_data
        gate_contour = density_gate_output.contour
        print('Plotting density plot and histogram...')
        density_params = {}
        density_params['mode'] = 'scatter'
        hist_params = {}
        hist_params['xlabel'] = ('FL1 ' + '(Molecules of Equivalent Fluorescein, MEFL)')
        plot_filename = '{}/density_hist_{}.png'.format(samples_plot_dir, 'S{:03}'.format((sample_id + 1)))
        FlowCal.plot.density_and_hist(sample, sample_gated, density_channels=['FSC', 'SSC'], hist_channels=['FL1'], gate_contour=gate_contour, density_params=density_params, hist_params=hist_params, savefig=plot_filename)
        samples.append(sample_gated)
    print('\nProcessing control samples...')
    min_sample = FlowCal.io.FCSData(min_sample_filename)
    max_sample = FlowCal.io.FCSData(max_sample_filename)
    min_sample = FlowCal.transform.to_rfi(min_sample)
    max_sample = FlowCal.transform.to_rfi(max_sample)
    min_sample = min_mef_transform_fxn(min_sample, channels=['FL1'])
    max_sample = max_mef_transform_fxn(max_sample, channels=['FL1'])
    min_sample_gated = FlowCal.gate.start_end(min_sample, num_start=250, num_end=100)
    max_sample_gated = FlowCal.gate.start_end(max_sample, num_start=250, num_end=100)
    min_sample_gated = FlowCal.gate.high_low(min_sample_gated, channels=['FSC', 'SSC', 'FL1'])
    max_sample_gated = FlowCal.gate.high_low(max_sample_gated, channels=['FSC', 'SSC', 'FL1'])
    min_density_gate_output = FlowCal.gate.density2d(data=min_sample_gated, channels=['FSC', 'SSC'], gate_fraction=0.85, full_output=True)
    min_sample_gated = min_density_gate_output.gated_data
    min_gate_contour = min_density_gate_output.contour
    max_density_gate_output = FlowCal.gate.density2d(data=max_sample_gated, channels=['FSC', 'SSC'], gate_fraction=0.85, full_output=True)
    max_sample_gated = max_density_gate_output.gated_data
    max_gate_contour = max_density_gate_output.contour
    min_plot_filename = '{}/density_hist_min.png'.format(samples_plot_dir)
    max_plot_filename = '{}/density_hist_max.png'.format(samples_plot_dir)
    FlowCal.plot.density_and_hist(min_sample, min_sample_gated, density_channels=['FSC', 'SSC'], hist_channels=['FL1'], gate_contour=min_gate_contour, density_params=density_params, hist_params=hist_params, savefig=min_plot_filename)
    FlowCal.plot.density_and_hist(max_sample, max_sample_gated, density_channels=['FSC', 'SSC'], hist_channels=['FL1'], gate_contour=max_gate_contour, density_params=density_params, hist_params=hist_params, savefig=max_plot_filename)
    cmap = mpl.cm.get_cmap('gray_r')
    norm = mpl.colors.LogNorm(vmin=1.0, vmax=3500.0)
    colors = [cmap(norm((dapg_i + 4.0))) for dapg_i in dapg]
    plt.figure(figsize=(6, 3.5))
    FlowCal.plot.hist1d(samples, channel='FL1', histtype='step', bins=128, edgecolor=colors)
    plt.ylim((0, 2500))
    plt.xlim((0, 50000.0))
    plt.xlabel('FL1  (Molecules of Equivalent Fluorescein, MEFL)')
    plt.legend(['{} $\\mu M$ DAPG'.format(i) for i in dapg], loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.savefig('histograms.png', dpi=200)
    plt.close()
    samples_fluorescence = [FlowCal.stats.mean(s, channels='FL1') for s in samples]
    min_fluorescence = FlowCal.stats.mean(min_sample_gated, channels='FL1')
    max_fluorescence = FlowCal.stats.mean(max_sample_gated, channels='FL1')
    dapg_color = '#ffc400'
    plt.figure(figsize=(3, 3))
    plt.plot(dapg, samples_fluorescence, marker='o', color=dapg_color)
    plt.axhline(min_fluorescence, color='gray', linestyle='--', zorder=(- 1))
    plt.text(s='Min', x=200.0, y=160.0, ha='left', va='bottom', color='gray')
    plt.axhline(max_fluorescence, color='gray', linestyle='--', zorder=(- 1))
    plt.text(s='Max', x=(- 0.7), y=5200.0, ha='left', va='top', color='gray')
    plt.yscale('log')
    plt.ylim((50.0, 10000.0))
    plt.xscale('symlog')
    plt.xlim(((- 1.0), 1000.0))
    plt.xlabel('DAPG Concentration ($\\mu M$)')
    plt.ylabel('FL1 Fluorescence (MEFL)')
    plt.tight_layout()
    plt.savefig('dose_response.png', dpi=200)
    plt.close()

    def dapg_sensor_output(dapg_concentration):
        mn = 86.0
        mx = 3147.0
        K = 20.0
        n = 3.57
        if (dapg_concentration <= 0):
            return mn
        else:
            return (mn + ((mx - mn) / (1 + ((K / dapg_concentration) ** n))))
    autofluorescence = FlowCal.stats.mean(min_sample_gated, channels='FL1')

    def dapg_sensor_cellular_fluorescence(dapg_concentration):
        return (dapg_sensor_output(dapg_concentration) + autofluorescence)
    plt.figure(figsize=(4, 3.5))
    FlowCal.plot.violin_dose_response(data=samples, channel='FL1', positions=dapg, min_data=min_sample_gated, max_data=max_sample_gated, model_fxn=dapg_sensor_cellular_fluorescence, violin_kwargs={'facecolor': dapg_color, 'edgecolor': 'black'}, violin_width_to_span_fraction=0.075, xscale='log', yscale='log', ylim=(10.0, 30000.0), draw_model_kwargs={'color': 'gray', 'linewidth': 3, 'zorder': (- 1), 'solid_capstyle': 'butt'})
    plt.xlabel('DAPG Concentration ($\\mu M$)')
    plt.ylabel('FL1 Fluorescence (MEFL)')
    plt.tight_layout()
    plt.savefig('dose_response_violin.png', dpi=200)
    plt.close()
    print('\nDone.')
