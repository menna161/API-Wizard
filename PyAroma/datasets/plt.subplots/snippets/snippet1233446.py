import copy
import matplotlib.pyplot as plt
import sys
from utils.vroom import solve


def plot_pareto_front(indicators, pareto_plot_file, full_Y_scale=False):
    (fig, ax1) = plt.subplots(1, 1)
    plt.xlabel('Completion time')
    plt.ylabel('Cost')
    options = {'dichotomy': {'marker': '^', 'edgecolor': 'red', 'linewidth': 0.7}, 'backward_search': {'marker': 'o', 'edgecolor': 'blue', 'linewidth': 0.5}}
    ymax = indicators[0]['cost']
    for origin in ['backward_search', 'dichotomy']:
        costs = [i['cost'] for i in indicators if (i['origin'] == origin)]
        if (len(costs) == 0):
            continue
        completions = [i['completion'] for i in indicators if (i['origin'] == origin)]
        ymax = max(ymax, max(costs))
        ax1.scatter(completions, costs, facecolor='none', edgecolor=options[origin]['edgecolor'], marker=options[origin]['marker'], linewidth=options[origin]['linewidth'])
    if full_Y_scale:
        ax1.set_ylim(0, (ymax * 1.05))
    plt.savefig(pareto_plot_file, bbox_inches='tight')
    plt.close()
