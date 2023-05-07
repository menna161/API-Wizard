import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib._color_data as mcd
from typing import Optional, List, Union, Dict, Tuple
from collections.abc import Iterable


def plot_pdos(self, ax: Optional[Axes]=None, to_plot: Optional[Dict[(str, List[str])]]=None, colors: Optional[Iterable]=None, plot_total_dos: Optional[bool]=True, xrange: Optional[Tuple[(float, float)]]=None, ymax: Optional[float]=None, scaling: Optional[Dict[(str, Dict[(str, float)])]]=None, split: bool=False, title: Optional[str]=None, title_loc: str='center', labels: bool=True, title_fontsize: int=16, legend_pos: str='outside') -> Figure:
    if (not ax):
        (fig, ax) = plt.subplots(1, 1, figsize=(8.0, 3.0))
    else:
        fig = None
    if (not colors):
        colors = mcd.TABLEAU_COLORS
    assert isinstance(colors, Iterable)
    color_iterator = (c for c in colors)
    if (not scaling):
        scaling = {}
    if xrange:
        e_range = ((self.energy >= xrange[0]) & (self.energy <= xrange[1]))
    else:
        e_range = np.ma.make_mask(self.energy)
    auto_ymax = 0.0
    if (not to_plot):
        to_plot = {}
        assert isinstance(self.species, Iterable)
        for s in set(self.species):
            to_plot[s] = ['s', 'p', 'd']
            if (self.lmax == 3):
                to_plot[s].append('f')
    for species in to_plot.keys():
        assert isinstance(self.species, Iterable)
        index = [i for (i, s) in enumerate(self.species) if (s == species)]
        for state in to_plot[species]:
            assert (state in ['s', 'p', 'd', 'f'])
            color = next(color_iterator)
            label = '{} {}'.format(species, state)
            up_dos = self.pdos_sum(atoms=index, l=state, spin='up')[e_range]
            down_dos = self.pdos_sum(atoms=index, l=state, spin='down')[e_range]
            if (species in scaling):
                if (state in scaling[species]):
                    up_dos *= scaling[species][state]
                    down_dos *= scaling[species][state]
                    label = '{} {} $\\times${}'.format(species, state, scaling[species][state])
            auto_ymax = max([auto_ymax, up_dos.max(), down_dos.max()])
            ax.plot(self.energy[e_range], up_dos, label=label, c=color)
            ax.plot(self.energy[e_range], (down_dos * (- 1.0)), c=color)
    if plot_total_dos:
        ax.fill_between(self.energy[e_range], self.tdos.up.values[e_range], (self.tdos.down.values[e_range] * (- 1.0)), facecolor=TABLEAU_GREY, alpha=0.2)
        auto_ymax = max([auto_ymax, self.tdos.up.values[e_range].max(), self.tdos.down.values[e_range].max()])
    if xrange:
        ax.set_xlim(xrange[0], xrange[1])
    if (not ymax):
        ymax = (1.1 * auto_ymax)
    ax.set_ylim(((- ymax) * 1.1), (ymax * 1.1))
    if (legend_pos == 'outside'):
        ax.legend(bbox_to_anchor=(1.01, 1.04), loc='upper left')
    else:
        ax.legend(loc=legend_pos)
    if labels:
        ax.set_xlabel('Energy [eV]')
    ax.axhline(y=0, c='lightgrey')
    ax.axes.grid(False, axis='y')
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    if title:
        ax.set_title(title, loc=title_loc, fontdict={'fontsize': title_fontsize})
    return fig
