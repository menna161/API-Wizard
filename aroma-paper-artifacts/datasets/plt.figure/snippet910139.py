import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import FlowCal

if (__name__ == '__main__'):
    instruments_table = FlowCal.excel_ui.read_table(filename='experiment.xlsx', sheetname='Instruments', index_col='ID')
    beads_table = FlowCal.excel_ui.read_table(filename='experiment.xlsx', sheetname='Beads', index_col='ID')
    samples_table = FlowCal.excel_ui.read_table(filename='experiment.xlsx', sheetname='Samples', index_col='ID')
    (beads_samples, mef_transform_fxns) = FlowCal.excel_ui.process_beads_table(beads_table=beads_table, instruments_table=instruments_table, verbose=True, plot=True, plot_dir='plot_beads')
    samples = FlowCal.excel_ui.process_samples_table(samples_table=samples_table, instruments_table=instruments_table, mef_transform_fxns=mef_transform_fxns, verbose=True, plot=True, plot_dir='plot_samples')
    sample_ids = ['S00{:02}'.format(n) for n in range(1, (10 + 1))]
    dapg = samples_table.loc[(sample_ids, 'DAPG (uM)')]
    cmap = mpl.cm.get_cmap('gray_r')
    norm = mpl.colors.LogNorm(vmin=1.0, vmax=3500.0)
    colors = [cmap(norm((dapg_i + 4.0))) for dapg_i in dapg]
    plt.figure(figsize=(6, 3.5))
    FlowCal.plot.hist1d([samples[s_id] for s_id in sample_ids], channel='FL1', histtype='step', bins=128, edgecolor=colors)
    plt.ylim((0, 2500))
    plt.xlim((0, 50000.0))
    plt.xlabel('FL1  (Molecules of Equivalent Fluorescein, MEFL)')
    plt.legend(['{:.1f} $\\mu M$ DAPG'.format(i) for i in dapg], loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.savefig('histograms.png', dpi=200)
    plt.close()
    samples_fluorescence = [FlowCal.stats.mean(samples[s_id], channels='FL1') for s_id in sample_ids]
    min_fluorescence = FlowCal.stats.mean(samples['min'], channels='FL1')
    max_fluorescence = FlowCal.stats.mean(samples['max'], channels='FL1')
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
    autofluorescence = FlowCal.stats.mean(samples['min'], channels='FL1')

    def dapg_sensor_cellular_fluorescence(dapg_concentration):
        return (dapg_sensor_output(dapg_concentration) + autofluorescence)
    plt.figure(figsize=(4, 3.5))
    FlowCal.plot.violin_dose_response(data=[samples[s_id] for s_id in sample_ids], channel='FL1', positions=dapg, min_data=samples['min'], max_data=samples['max'], model_fxn=dapg_sensor_cellular_fluorescence, violin_kwargs={'facecolor': dapg_color, 'edgecolor': 'black'}, violin_width_to_span_fraction=0.075, xscale='log', yscale='log', ylim=(10.0, 30000.0), draw_model_kwargs={'color': 'gray', 'linewidth': 3, 'zorder': (- 1), 'solid_capstyle': 'butt'})
    plt.xlabel('DAPG Concentration ($\\mu M$)')
    plt.ylabel('FL1 Fluorescence (MEFL)')
    plt.tight_layout()
    plt.savefig('dose_response_violin.png', dpi=200)
    plt.close()
    print('\nDone.')
