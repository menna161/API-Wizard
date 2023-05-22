import os
from pathlib import Path
from tensorboard.backend.event_processing import event_accumulator
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib
import json


def plot(exp_path, step='sample_frames'):
    exp_path = Path(exp_path)
    (results, demo_returns) = get_results(exp_path)
    if ('sample_frames' == step):
        x = 'samples'
    elif ('sample_episodes' == step):
        x = 'episodes'
    elif ('train_steps' == step):
        x = 'steps'
    elif ('minutes' == step):
        x = 'minutes'
    else:
        raise ValueError("Invalid argument 'step'. step must be from            [sample_frames, sample_episodes, train_steps, minutes]")
    num_cols = len(results)
    (fig, axes) = plt.subplots(1, num_cols, figsize=((num_cols * 6), 4))
    if (num_cols == 1):
        axes = [axes]
    sns.set(style='darkgrid')
    colors = sns.color_palette()
    agents = []
    for (i, env) in enumerate(results):
        xlim = 0
        for agent in results[env]:
            df = results[env][agent][step]
            if (agent not in agents):
                agents.append(agent)
            sns.lineplot(x=x, y='return', ci='sd', data=df, ax=axes[i], label=agent, legend=None, color=colors[agents.index(agent)])
            xlim = max(xlim, df[x].max())
        axes[i].set_title(env)
        axes[i].set_xlim(0, xlim)
        demo_return = demo_returns[env]
        if (demo_return is not None):
            if ('Demonstration' not in agents):
                agents.append('Demonstration')
            axes[i].axhline(demo_return, ls='--', label='Demonstration', color=colors[agents.index('Demonstration')])
    handles = ([None] * len(agents))
    for ax in axes:
        (handle, label) = ax.get_legend_handles_labels()
        for (h, agent) in zip(handle, label):
            handles[agents.index(agent)] = h
    lgd = fig.legend(handles, agents, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(agents))
    fig.tight_layout()
    fig.savefig(str((exp_path / 'result.png')), bbox_extra_artists=(lgd,), bbox_inches='tight')
