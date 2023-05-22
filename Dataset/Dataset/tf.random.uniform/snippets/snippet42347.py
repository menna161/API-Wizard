import tensorflow as tf
import numpy as np

if (__name__ == '__main__'):
    batch_size = 8
    nclass = 10
    y_true = tf.random.uniform((batch_size,), 0, nclass, dtype=tf.int32)
    y_pred = tf.random.uniform((batch_size, nclass), (- 1), 1, dtype=tf.float32)
    batch_idxs = tf.expand_dims(tf.range(0, batch_size, dtype=tf.int32), 1)
    idxs = tf.concat([batch_idxs, tf.cast(tf.expand_dims(y_true, (- 1)), tf.int32)], 1)
    mask = tf.logical_not(tf.scatter_nd(idxs, tf.ones(tf.shape(idxs)[0], tf.bool), tf.shape(y_pred)))
    sp = tf.expand_dims(tf.gather_nd(y_pred, idxs), 1)
    sn = tf.reshape(tf.boolean_mask(y_pred, mask), (batch_size, (- 1)))
    circleloss = CircleLoss()
    sparsecircleloss = SparseCircleLoss(batch_size=batch_size)
    paircircleloss = PairCircleLoss()
    print('circle loss:\n', circleloss.call(tf.one_hot(y_true, nclass, dtype=tf.float32), y_pred).numpy())
    print('sparse circle loss:\n', sparsecircleloss.call(tf.expand_dims(y_true, (- 1)), y_pred).numpy().ravel())
    print('pair circle loss:\n', paircircleloss.call(sp, sn).numpy().ravel())
