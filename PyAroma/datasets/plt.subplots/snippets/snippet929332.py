from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from dreamer.tools import count_dataset
from dreamer.tools import gif_summary
from dreamer.tools import image_strip_summary
from dreamer.tools import shape as shapelib


def body_fn(lines):
    (fig, axes) = plt.subplots(nrows=len(titles), ncols=1, sharex=True, sharey=False, squeeze=False, figsize=(6, (3 * len(lines))))
    axes = axes[(:, 0)]
    for (index, ax) in enumerate(axes):
        ax.set_title(titles[index])
        for (line, label) in zip(lines[index], labels[index]):
            ax.plot(line, label=label)
        if any(labels[index]):
            ax.legend(frameon=False)
    fig.tight_layout()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape((fig.canvas.get_width_height()[::(- 1)] + (3,)))
    plt.close(fig)
    return image
