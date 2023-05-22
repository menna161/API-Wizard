import abc
import typing
from pathlib import Path
import dill
import numpy as np
import keras
import keras.backend as K
import pandas as pd
import matchzoo
from matchzoo import DataGenerator
from matchzoo.engine import hyper_spaces
from matchzoo.engine.base_preprocessor import BasePreprocessor
from matchzoo.engine.base_metric import BaseMetric
from matchzoo.engine.param_table import ParamTable
from matchzoo.engine.param import Param
from matchzoo import tasks


def evaluate(self, x: typing.Dict[(str, np.ndarray)], y: np.ndarray, batch_size: int=128) -> typing.Dict[(BaseMetric, float)]:
    "\n        Evaluate the model.\n\n        :param x: Input data.\n        :param y: Labels.\n        :param batch_size: Number of samples when `predict` for evaluation.\n            (default: 128)\n\n        Examples::\n            >>> import matchzoo as mz\n            >>> data_pack = mz.datasets.toy.load_data()\n            >>> preprocessor = mz.preprocessors.NaivePreprocessor()\n            >>> data_pack = preprocessor.fit_transform(data_pack, verbose=0)\n            >>> m = mz.models.DenseBaseline()\n            >>> m.params['task'] = mz.tasks.Ranking()\n            >>> m.params['task'].metrics = [\n            ...     'acc', 'mse', 'mae', 'ce',\n            ...     'average_precision', 'precision', 'dcg', 'ndcg',\n            ...     'mean_reciprocal_rank', 'mean_average_precision', 'mrr',\n            ...     'map', 'MAP',\n            ...     mz.metrics.AveragePrecision(threshold=1),\n            ...     mz.metrics.Precision(k=2, threshold=2),\n            ...     mz.metrics.DiscountedCumulativeGain(k=2),\n            ...     mz.metrics.NormalizedDiscountedCumulativeGain(\n            ...         k=3, threshold=-1),\n            ...     mz.metrics.MeanReciprocalRank(threshold=2),\n            ...     mz.metrics.MeanAveragePrecision(threshold=3)\n            ... ]\n            >>> m.guess_and_fill_missing_params(verbose=0)\n            >>> m.build()\n            >>> m.compile()\n            >>> x, y = data_pack.unpack()\n            >>> evals = m.evaluate(x, y)\n            >>> type(evals)\n            <class 'dict'>\n\n        "
    result = dict()
    (matchzoo_metrics, keras_metrics) = self._separate_metrics()
    y_pred = self.predict(x, batch_size)
    for metric in keras_metrics:
        metric_func = keras.metrics.get(metric)
        result[metric] = K.eval(K.mean(metric_func(K.variable(y), K.variable(y_pred))))
    if matchzoo_metrics:
        if (not isinstance(self.params['task'], tasks.Ranking)):
            raise ValueError('Matchzoo metrics only works on ranking.')
        for metric in matchzoo_metrics:
            result[metric] = self._eval_metric_on_data_frame(metric, x['id_left'], y, y_pred)
    return result
