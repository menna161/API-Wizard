from tensorflow.python.eager import context
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import tensor_shape
from tensorflow.python.framework import tensor_util
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.python.ops import tensor_array_ops
from tensorflow.python.ops import variable_scope as vs
from tensorflow.python.util import nest
from tensorflow.python.util.tf_export import tf_export
from tensorflow.python.ops import rnn
import pdb


def bidirectional_dynamic_rnn_2inputs_time_input(cell_fw, cell_bw, inputs_fw, inputs_bw, sequence_length=None, time_input_for_fw=True, time_input_for_bw=True, initial_state_fw=None, initial_state_bw=None, dtype=None, parallel_iterations=None, swap_memory=False, time_major=False, scope=None):
    'Creates a dynamic version of bidirectional recurrent neural network, add current\n  time to input of cell. A different input for forward and backward direction are used,\n  which means they are actually fully decoupled, and 2 unidirectional RNNs could be used.\n  For sake of concistency, we allow this function as well.\n  Takes input and builds independent forward and backward RNNs. The input_size\n  of forward and backward cell must match. The initial state for both directions\n  is zero by default (but can be set optionally) and no intermediate states are\n  ever returned -- the network is fully unrolled for the given (passed in)\n  length(s) of the sequence(s) or completely unrolled if length(s) is not\n  given.\n  Args:\n    cell_fw: An instance of RNNCell, to be used for forward direction.\n    cell_bw: An instance of RNNCell, to be used for backward direction.\n    inputs_fw: The RNN inputs for forward direction.\n      If time_major == False (default), this must be a tensor of shape:\n        `[batch_size, max_time, ...]`, or a nested tuple of such elements.\n      If time_major == True, this must be a tensor of shape:\n        `[max_time, batch_size, ...]`, or a nested tuple of such elements.\n    inputs_bw: The RNN inputs for backward direction.\n    sequence_length: (optional) An int32/int64 vector, size `[batch_size]`,\n      containing the actual lengths for each of the sequences in the batch.\n      If not provided, all batch entries are assumed to be full sequences; and\n      time reversal is applied from time `0` to `max_time` for each sequence.\n    initial_state_fw: (optional) An initial state for the forward RNN.\n      This must be a tensor of appropriate type and shape\n      `[batch_size, cell_fw.state_size]`.\n      If `cell_fw.state_size` is a tuple, this should be a tuple of\n      tensors having shapes `[batch_size, s] for s in cell_fw.state_size`.\n    initial_state_bw: (optional) Same as for `initial_state_fw`, but using\n      the corresponding properties of `cell_bw`.\n    dtype: (optional) The data type for the initial states and expected output.\n      Required if initial_states are not provided or RNN states have a\n      heterogeneous dtype.\n    parallel_iterations: (Default: 32).  The number of iterations to run in\n      parallel.  Those operations which do not have any temporal dependency\n      and can be run in parallel, will be.  This parameter trades off\n      time for space.  Values >> 1 use more memory but take less time,\n      while smaller values use less memory but computations take longer.\n    swap_memory: Transparently swap the tensors produced in forward inference\n      but needed for back prop from GPU to CPU.  This allows training RNNs\n      which would typically not fit on a single GPU, with very minimal (or no)\n      performance penalty.\n    time_major: The shape format of the `inputs` and `outputs` Tensors.\n      If true, these `Tensors` must be shaped `[max_time, batch_size, depth]`.\n      If false, these `Tensors` must be shaped `[batch_size, max_time, depth]`.\n      Using `time_major = True` is a bit more efficient because it avoids\n      transposes at the beginning and end of the RNN calculation.  However,\n      most TensorFlow data is batch-major, so by default this function\n      accepts input and emits output in batch-major form.\n    scope: VariableScope for the created subgraph; defaults to\n      "bidirectional_rnn"\n  Returns:\n    A tuple (outputs, output_states) where:\n      outputs: A tuple (output_fw, output_bw) containing the forward and\n        the backward rnn output `Tensor`.\n        If time_major == False (default),\n          output_fw will be a `Tensor` shaped:\n          `[batch_size, max_time, cell_fw.output_size]`\n          and output_bw will be a `Tensor` shaped:\n          `[batch_size, max_time, cell_bw.output_size]`.\n        If time_major == True,\n          output_fw will be a `Tensor` shaped:\n          `[max_time, batch_size, cell_fw.output_size]`\n          and output_bw will be a `Tensor` shaped:\n          `[max_time, batch_size, cell_bw.output_size]`.\n        It returns a tuple instead of a single concatenated `Tensor`, unlike\n        in the `bidirectional_rnn`. If the concatenated one is preferred,\n        the forward and backward outputs can be concatenated as\n        `tf.concat(outputs, 2)`.\n      output_states: A tuple (output_state_fw, output_state_bw) containing\n        the forward and the backward final states of bidirectional rnn.\n  Raises:\n    TypeError: If `cell_fw` or `cell_bw` is not an instance of `RNNCell`.\n  '
    rnn_cell_impl.assert_like_rnncell('cell_fw', cell_fw)
    rnn_cell_impl.assert_like_rnncell('cell_bw', cell_bw)
    with vs.variable_scope((scope or 'bidirectional_rnn')):
        with vs.variable_scope('fw') as fw_scope:
            if time_input_for_fw:
                dynamic_rnn_fw_type = dynamic_rnn_time_input
            else:
                dynamic_rnn_fw_type = rnn.dynamic_rnn
            (output_fw, output_state_fw) = dynamic_rnn_fw_type(cell=cell_fw, inputs=inputs_fw, sequence_length=sequence_length, initial_state=initial_state_fw, dtype=dtype, parallel_iterations=parallel_iterations, swap_memory=swap_memory, time_major=time_major, scope=fw_scope)
        if (not time_major):
            time_dim = 1
            batch_dim = 0
        else:
            time_dim = 0
            batch_dim = 1

        def _reverse(input_, seq_lengths, seq_axis, batch_axis):
            if (seq_lengths is not None):
                return array_ops.reverse_sequence(input=input_, seq_lengths=seq_lengths, seq_axis=seq_axis, batch_axis=batch_axis)
            else:
                return array_ops.reverse(input_, axis=[seq_axis])
        with vs.variable_scope('bw') as bw_scope:
            inputs_reverse = _reverse(inputs_bw, seq_lengths=sequence_length, seq_axis=time_dim, batch_axis=batch_dim)
            if time_input_for_bw:
                dynamic_rnn_bw_type = dynamic_rnn_time_input
            else:
                dynamic_rnn_bw_type = rnn.dynamic_rnn
            (tmp, output_state_bw) = dynamic_rnn_bw_type(cell=cell_bw, inputs=inputs_reverse, sequence_length=sequence_length, initial_state=initial_state_bw, dtype=dtype, parallel_iterations=parallel_iterations, swap_memory=swap_memory, time_major=time_major, scope=bw_scope)
    if (type(tmp) == tuple):
        output_bw = tuple((_reverse(tmp_i, seq_lengths=sequence_length, seq_axis=time_dim, batch_axis=batch_dim) for tmp_i in tmp))
    else:
        output_bw = _reverse(tmp, seq_lengths=sequence_length, seq_axis=time_dim, batch_axis=batch_dim)
    outputs = (output_fw, output_bw)
    output_states = (output_state_fw, output_state_bw)
    return (outputs, output_states)
