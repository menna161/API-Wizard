from leather.axis import Axis
from leather.chart import Chart
from leather.data_types import Date, DateTime
from leather.grid import Grid
from leather.scales import Linear, Scale, Temporal
from leather.series import Series
from leather.shapes import Line
from leather.utils import X, Y


def add_x_scale(self, domain_min, domain_max):
    '\n        Create and add a :class:`.Scale`.\n\n        If the provided domain values are :class:`date` or :class:`datetime`\n        then a :class:`.Temporal` scale will be created, otherwise it will\n        :class:`.Linear`.\n\n        If you want to set a custom scale class use :meth:`.Lattice.set_x_scale`\n        instead.\n        '
    scale_type = Linear
    if (isinstance(domain_min, Date.types) or isinstance(domain_min, DateTime.types)):
        scale_type = Temporal
    self.set_x_scale(scale_type(domain_min, domain_max))
