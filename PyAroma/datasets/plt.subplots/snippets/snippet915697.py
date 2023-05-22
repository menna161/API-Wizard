from contextlib import contextmanager
import matplotlib.pyplot as plt


@contextmanager
def canvas(image_file=None, **kwargs):
    'Generic matplotlib context.'
    (fig, ax) = plt.subplots(**kwargs)
    (yield ax)
    fig.set_tight_layout(True)
    if image_file:
        fig.savefig(image_file, dpi=300)
    fig.show()
    plt.close(fig)
