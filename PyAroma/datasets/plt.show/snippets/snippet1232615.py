import numpy as np
from PIL import Image
from argparse import ArgumentParser
from pathlib import Path
from constants import LEVELS, PERTURBATIONS
import matplotlib
import matplotlib.pyplot as plt


def visualize(img, perturbations, levels, show):
    'Visualize all specified perturbations and levels for a given image.\n\n    Args:\n        img (Image): PIL image for which to plot perturbations\n        perturbations (dict): maps name (str) -> mapping function (function)\n        levels (list): list of each level (int) to plot\n        show (bool): whether to show the final figure\n\n    Returns:\n        (None)\n\n    '
    import matplotlib
    if (not show):
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    out_dir = Path('output')
    out_dir.mkdir(exist_ok=True, parents=True)
    if ('identity' in perturbations):
        perturbations = perturbations.copy()
        del perturbations['identity']
    (fig, ax) = plt.subplots(nrows=len(levels), ncols=len(perturbations), gridspec_kw={'wspace': 0, 'hspace': 0}, figsize=FIG_SIZE)
    names = sorted(list(perturbations.keys()))
    for (iname, name) in enumerate(names):
        print(('Generating visuals for "%s"...' % name))
        mapping_fn = perturbations[name]
        for (ilevel, level) in enumerate(levels):
            perturbed_img = mapping_fn(level, img)
            perturbed_img_name = ('%s_%d.png' % (name, level))
            perturbed_img.save((out_dir / perturbed_img_name))
            ax[(ilevel, iname)].imshow(perturbed_img)
            ax[(ilevel, iname)].set_yticklabels([])
            ax[(ilevel, iname)].set_xticklabels([])
            ax[(ilevel, iname)].tick_params(axis='both', which='both', length=0)
            if (not iname):
                ax[(ilevel, iname)].set_ylabel(('Level %d' % level), rotation=90, size='large')
            if (not ilevel):
                ax[(ilevel, iname)].set_title(name)
    if show:
        plt.show()
    plt.savefig((out_dir / 'visualization.png'))
