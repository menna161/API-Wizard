from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import contextlib
import multiprocessing
import numpy as np
import pandas as pd
import tensorflow as tf
from official.utils.data import file_io


def _serialize_deserialize(self, num_cores=1, num_rows=20):
    np.random.seed(1)
    df = pd.DataFrame({_RAW_ROW: np.array(range(num_rows), dtype=np.int64), _DUMMY_COL: np.random.randint(0, 35, size=(num_rows,)), _DUMMY_VEC_COL: [np.array([np.random.random() for _ in range(_DUMMY_VEC_LEN)]) for i in range(num_rows)]})
    with fixed_core_count(num_cores):
        buffer_path = file_io.write_to_temp_buffer(df, self.get_temp_dir(), [_RAW_ROW, _DUMMY_COL, _DUMMY_VEC_COL])
    with self.test_session(graph=tf.Graph()) as sess:
        dataset = tf.data.TFRecordDataset(buffer_path)
        dataset = dataset.batch(1).map((lambda x: tf.parse_example(x, _FEATURE_MAP)))
        data_iter = dataset.make_one_shot_iterator()
        seen_rows = set()
        for i in range((num_rows + 5)):
            row = data_iter.get_next()
            try:
                (row_id, val_0, val_1) = sess.run([row[_RAW_ROW], row[_DUMMY_COL], row[_DUMMY_VEC_COL]])
                (row_id, val_0, val_1) = (row_id[0][0], val_0[0][0], val_1[0])
                assert (row_id not in seen_rows)
                seen_rows.add(row_id)
                self.assertEqual(val_0, df[_DUMMY_COL][row_id])
                self.assertAllClose(val_1, df[_DUMMY_VEC_COL][row_id])
                self.assertLess(i, num_rows, msg='Too many rows.')
            except tf.errors.OutOfRangeError:
                self.assertGreaterEqual(i, num_rows, msg='Too few rows.')
    file_io._GARBAGE_COLLECTOR.purge()
    assert (not tf.gfile.Exists(buffer_path))
