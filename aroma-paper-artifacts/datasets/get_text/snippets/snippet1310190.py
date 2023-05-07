from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureCanvasBase, FigureManagerBase, GraphicsContextBase, RendererBase
from matplotlib.figure import Figure


def get_text_width_height_descent(self, s, prop, ismath):
    return (1, 1, 1)
