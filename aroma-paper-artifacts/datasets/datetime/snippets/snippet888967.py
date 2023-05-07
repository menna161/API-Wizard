import os
import xml.etree.ElementTree as ET
import leather.svg as svg
from leather import theme
from leather.axis import Axis
from leather.data_types import Date, DateTime
from leather.scales import Linear, Scale, Temporal
from leather.series import CategorySeries, Series
from leather.shapes import Bars, Columns, Dots, Line
from leather.utils import DIMENSION_NAMES, Box, IPythonSVG, X, Y, warn


def add_x_scale(self, domain_min, domain_max):
    '\n        Create and add a :class:`.Scale`.\n\n        If the provided domain values are :class:`date` or :class:`datetime`\n        then a :class:`.Temporal` scale will be created, otherwise it will\n        :class:`.Linear`.\n\n        If you want to set a custom scale class use :meth:`.Chart.set_x_scale`\n        instead.\n        '
    scale_type = Linear
    if (isinstance(domain_min, Date.types) or isinstance(domain_min, DateTime.types)):
        scale_type = Temporal
    self.set_x_scale(scale_type(domain_min, domain_max))
