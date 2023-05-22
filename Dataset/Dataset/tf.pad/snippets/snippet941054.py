import tensorflow as tf
from configuration import VARIANCE, NMS_THRESHOLD, CONFIDENCE_THRESHOLD, MAX_BOXES_NUM
from core.anchor import DefaultBoxes


def __call__(self, inputs, *args, **kwargs):
    (loc_data, conf_data) = self.model(inputs, training=False)
    conf_data = tf.nn.softmax(conf_data)
    batch_size = loc_data.shape[0]
    num_priors = self.priors.shape[0]
    conf_preds = tf.transpose(a=conf_data, perm=[0, 2, 1])
    output = list()
    for i in range(batch_size):
        decoded_boxes = InferenceProcedure._decode(loc_data[i], self.priors, self.variance)
        conf_scores = conf_preds[i]
        t1 = list()
        t1.append(tf.zeros(shape=(self.top_k, 6)))
        for cl in range(1, self.num_classes):
            c_mask = tf.math.greater(conf_scores[cl], self.conf_thresh)
            scores = tf.boolean_mask(conf_scores[cl], c_mask)
            if (scores.shape[0] == 0):
                continue
            l_mask = tf.broadcast_to(tf.expand_dims(c_mask, axis=1), shape=decoded_boxes.shape)
            boxes = tf.reshape(tf.boolean_mask(decoded_boxes, l_mask), shape=((- 1), 4))
            selected_indices = tf.image.non_max_suppression(boxes=boxes, scores=scores, max_output_size=self.top_k, iou_threshold=self.nms_thresh)
            selected_boxes = tf.gather(params=boxes, indices=selected_indices)
            num_boxes = selected_boxes.shape[0]
            selected_boxes = tf.pad(tensor=selected_boxes, paddings=[[0, (self.top_k - num_boxes)], [0, 0]])
            selected_scores = tf.expand_dims(tf.gather(params=scores, indices=selected_indices), axis=1)
            selected_scores = tf.pad(tensor=selected_scores, paddings=[[0, (self.top_k - num_boxes)], [0, 0]])
            selected_classes = tf.fill(dims=[self.top_k, 1], value=cl)
            selected_classes = tf.cast(selected_classes, dtype=tf.float32)
            targets = tf.concat(values=[selected_scores, selected_boxes, selected_classes], axis=1)
            t1.append(targets)
        t2 = tf.stack(values=t1, axis=0)
        output.append(t2)
    output = tf.stack(values=output, axis=0)
    flt = tf.reshape(output, shape=(batch_size, (- 1), 6))
    idx = tf.argsort(values=flt[(:, :, 0)], axis=1, direction='DESCENDING')
    rank = tf.argsort(values=idx, axis=1, direction='ASCENDING')
    mask = (rank < self.top_k)
    mask = tf.expand_dims(mask, axis=(- 1))
    mask = tf.broadcast_to(mask, shape=flt.shape)
    flt = tf.where(condition=mask, x=0, y=flt)
    return tf.reshape(flt, shape=(batch_size, (- 1), self.top_k, 6))
