from datetime import date, datetime
from leather.data_types import Date, DateTime, Number, Text
from leather.shapes import Bars, Columns
from leather.scales.linear import Linear
from leather.scales.ordinal import Ordinal
from leather.scales.temporal import Temporal


@classmethod
def infer(cls, layers, dimension, data_type):
    "\n        Infer's an appropriate default scale for a given sequence of\n        :class:`.Series`.\n\n        :param chart_series:\n            A sequence of :class:`.Series` instances\n        :param dimension:\n            The dimension, :code:`X` or :code:`Y` of the data to infer for.\n        :param data_type:\n            The type of data contained in the series dimension.\n        "
    from leather.scales.linear import Linear
    from leather.scales.ordinal import Ordinal
    from leather.scales.temporal import Temporal
    if (data_type is Date):
        data_min = date.max
        data_max = date.min
        for (series, shape) in layers:
            data_min = min(data_min, series.min(dimension))
            data_max = max(data_max, series.max(dimension))
        scale = Temporal(data_min, data_max)
    elif (data_type is DateTime):
        data_min = datetime.max
        data_max = datetime.min
        for (series, shape) in layers:
            data_min = min(data_min, series.min(dimension))
            data_max = max(data_max, series.max(dimension))
        scale = Temporal(data_min, data_max)
    elif (data_type is Number):
        force_zero = False
        data_min = None
        data_max = None
        for (series, shape) in layers:
            if isinstance(shape, (Bars, Columns)):
                force_zero = True
            if (data_min is None):
                data_min = series.min(dimension)
            else:
                data_min = min(data_min, series.min(dimension))
            if (data_max is None):
                data_max = series.max(dimension)
            else:
                data_max = max(data_max, series.max(dimension))
        if force_zero:
            if (data_min > 0):
                data_min = 0
            if (data_max < 0):
                data_max = 0
        scale = Linear(data_min, data_max)
    elif (data_type is Text):
        scale_values = None
        if (len(layers) == 1):
            scale_values = layers[0][0].values(dimension)
        else:
            first_series = set(layers[0][0].values(dimension))
            data_series = [series.values(dimension) for (series, shape) in layers]
            all_same = True
            for series in data_series:
                if (set(series) != first_series):
                    all_same = False
                    break
            if all_same:
                scale_values = layers[0][0].values(dimension)
            else:
                scale_values = sorted(set().union(*data_series))
        scale = Ordinal(scale_values)
    return scale
