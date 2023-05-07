import uuid
import datetime as dt
from functools import reduce
import logging
import inspect
from .io import Input, Output, get_if_exists
from .errors import PyungoError
from .utils import get_function_return_names
from .data import Data
import jsonschema
from multiprocess import Pool


def calculate(self, data):
    ' run graph calculations '
    if self._schema:
        try:
            import jsonschema
        except ImportError:
            msg = 'jsonschema package is needed for validating data'
            raise ImportError(msg)
        jsonschema.validate(instance=data, schema=self._schema)
    t1 = dt.datetime.utcnow()
    LOGGER.info('Starting calculation...')
    dt1 = dt.datetime.utcnow()
    self._data = Data(data, do_deepcopy=self._do_deepcopy)
    dt2 = dt.datetime.utcnow()
    data_copy_time = (dt2 - dt1)
    self._data.check_inputs(self.sim_inputs, self.sim_outputs, self.sim_kwargs)
    if (not self._sorted_dep):
        self._topological_sort()
    for items in self._sorted_dep:
        for item in items:
            node = self._get_node(item)
            inputs = [i for i in node.inputs_without_constants]
            for inp in inputs:
                if ((not inp.is_kwarg) or (inp.is_kwarg and (inp.map in self._data._inputs))):
                    node.set_value_to_input(inp.name, self._data[inp.map])
                else:
                    node.set_value_to_input(inp.name, node._kwargs_default[inp.name])
        if self._parallel:
            try:
                from multiprocess import Pool
            except ImportError:
                msg = 'multiprocess package is needed for parralelism'
                raise ImportError(msg)
            pool = Pool(self._pool_size)
            results = pool.map(Graph.run_node, [self._get_node(i) for i in items])
            pool.close()
            pool.join()
            results = {k: v for (k, v) in results}
        else:
            results = {}
            for item in items:
                node = self._get_node(item)
                res = node.run_with_loaded_inputs()
                results[node.id] = res
        for item in items:
            node = self._get_node(item)
            res = results[node.id]
            if (len(node.outputs) == 1):
                self._data[node.outputs[0].map] = res
            else:
                for (i, out) in enumerate(node.outputs):
                    self._data[out.map] = res[i]
    t2 = dt.datetime.utcnow()
    total_compute_time = (t2 - t1)
    LOGGER.info('Calculation finished in {}'.format(total_compute_time))
    total_compute_time_seconds = total_compute_time.total_seconds()
    if (total_compute_time_seconds > 0):
        data_copy_perc = (data_copy_time.total_seconds() / total_compute_time.total_seconds())
    else:
        data_copy_perc = 0
    if (data_copy_perc > COPY_TIME_MAX_PERCENTAGE):
        msg = 'Data copy time was {} that is {:.1f}% of a total time of {}. Consider using do_deepcopy=False during the graph instantiation.'
        LOGGER.warning(msg.format(data_copy_time, (data_copy_perc * 100), total_compute_time))
    return res
