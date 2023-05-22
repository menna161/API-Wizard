import argparse
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_curve(log_dicts, args):
    if (args.backend is not None):
        plt.switch_backend(args.backend)
    sns.set_style(args.style)
    legend = args.legend
    if (legend is None):
        legend = []
        for json_log in args.json_logs:
            for metric in args.keys:
                legend.append('{}_{}'.format(json_log, metric))
    assert (len(legend) == (len(args.json_logs) * len(args.keys)))
    metrics = args.keys
    num_metrics = len(metrics)
    for (i, log_dict) in enumerate(log_dicts):
        epochs = list(log_dict.keys())
        for (j, metric) in enumerate(metrics):
            print('plot curve of {}, metric is {}'.format(args.json_logs[i], metric))
            assert (metric in log_dict[epochs[0]]), '{} does not contain metric {}'.format(args.json_logs[i], metric)
            if ('mAP' in metric):
                xs = np.arange(1, (max(epochs) + 1))
                ys = []
                for epoch in epochs:
                    ys += log_dict[epoch][metric]
                ax = plt.gca()
                ax.set_xticks(xs)
                plt.xlabel('epoch')
                plt.plot(xs, ys, label=legend[((i * num_metrics) + j)], marker='o')
            else:
                xs = []
                ys = []
                num_iters_per_epoch = log_dict[epochs[0]]['iter'][(- 1)]
                for epoch in epochs:
                    iters = log_dict[epoch]['iter']
                    if (log_dict[epoch]['mode'][(- 1)] == 'val'):
                        iters = iters[:(- 1)]
                    xs.append((np.array(iters) + ((epoch - 1) * num_iters_per_epoch)))
                    ys.append(np.array(log_dict[epoch][metric][:len(iters)]))
                xs = np.concatenate(xs)
                ys = np.concatenate(ys)
                plt.xlabel('iter')
                plt.plot(xs, ys, label=legend[((i * num_metrics) + j)], linewidth=0.5)
            plt.legend()
        if (args.title is not None):
            plt.title(args.title)
    if (args.out is None):
        plt.show()
    else:
        print('save curve to: {}'.format(args.out))
        plt.savefig(args.out)
        plt.cla()
