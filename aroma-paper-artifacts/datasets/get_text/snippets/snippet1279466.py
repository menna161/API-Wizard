from matplotlib.backend_bases import RendererBase
from matplotlib import colors as mcolors
from matplotlib import patches as mpatches
from matplotlib import transforms as mtransforms


def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
    (path, transform) = self._get_text_path_transform(x, y, s, prop, angle, ismath)
    color = gc.get_rgb()
    gc.set_linewidth(0.0)
    self.draw_path(gc, path, transform, rgbFace=color)
