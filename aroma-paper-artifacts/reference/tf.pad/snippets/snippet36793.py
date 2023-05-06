import tensorflow as tf


def filter_detections(boxes, classification, other=[], class_specific_filter=True, nms=True, score_threshold=0.05, max_detections=300, nms_threshold=0.5):
    " Filter detections using the boxes and classification values.\n\tArgs\n\t\tboxes                 : Tensor of shape (num_boxes, 4) containing the boxes in (x1, y1, x2, y2) format.\n\t\tclassification        : Tensor of shape (num_boxes, num_classes) containing the classification scores.\n\t\tother                 : List of tensors of shape (num_boxes, ...) to filter along with the boxes and classification scores.\n\t\tclass_specific_filter : Whether to perform filtering per class, or take the best scoring class and filter those.\n\t\tnms                   : Flag to enable/disable non maximum suppression.\n\t\tscore_threshold       : Threshold used to prefilter the boxes with.\n\t\tmax_detections        : Maximum number of detections to keep.\n\t\tnms_threshold         : Threshold for the IoU value to determine when a box should be suppressed.\n\tReturns\n\t\tA list of [boxes, scores, labels, other[0], other[1], ...].\n\t\tboxes is shaped (max_detections, 4) and contains the (x1, y1, x2, y2) of the non-suppressed boxes.\n\t\tscores is shaped (max_detections,) and contains the scores of the predicted class.\n\t\tlabels is shaped (max_detections,) and contains the predicted label.\n\t\tother[i] is shaped (max_detections, ...) and contains the filtered other[i] data.\n\t\tIn case there are less than max_detections detections, the tensors are padded with -1's.\n\t"

    def _filter_detections(scores, labels):
        indices = tf.where(tf.keras.backend.greater(scores, score_threshold))
        if nms:
            filtered_boxes = tf.gather_nd(boxes, indices)
            filtered_scores = tf.keras.backend.gather(scores, indices)[(:, 0)]
            nms_indices = tf.image.non_max_suppression(filtered_boxes, filtered_scores, max_output_size=max_detections, iou_threshold=nms_threshold)
            indices = tf.keras.backend.gather(indices, nms_indices)
        labels = tf.gather_nd(labels, indices)
        indices = tf.keras.backend.stack([indices[(:, 0)], labels], axis=1)
        return indices
    if class_specific_filter:
        all_indices = []
        for c in range(int(classification.shape[1])):
            scores = classification[(:, c)]
            labels = (c * tf.ones((tf.keras.backend.shape(scores)[0],), dtype='int64'))
            all_indices.append(_filter_detections(scores, labels))
        indices = tf.keras.backend.concatenate(all_indices, axis=0)
    else:
        scores = tf.keras.backend.max(classification, axis=1)
        labels = tf.keras.backend.argmax(classification, axis=1)
        indices = _filter_detections(scores, labels)
    scores = tf.gather_nd(classification, indices)
    labels = indices[(:, 1)]
    (scores, top_indices) = tf.nn.top_k(scores, k=tf.keras.backend.minimum(max_detections, tf.keras.backend.shape(scores)[0]))
    scores = tf.stop_gradient(scores)
    top_indices = tf.stop_gradient(top_indices)
    indices = tf.keras.backend.gather(indices[(:, 0)], top_indices)
    boxes = tf.keras.backend.gather(boxes, indices)
    labels = tf.keras.backend.gather(labels, top_indices)
    other_ = [tf.keras.backend.gather(o, indices) for o in other]
    pad_size = tf.keras.backend.maximum(0, (max_detections - tf.keras.backend.shape(scores)[0]))
    boxes = tf.pad(boxes, [[0, pad_size], [0, 0]], constant_values=(- 1))
    scores = tf.pad(scores, [[0, pad_size]], constant_values=(- 1))
    labels = tf.pad(labels, [[0, pad_size]], constant_values=(- 1))
    labels = tf.keras.backend.cast(labels, 'int32')
    other_ = [tf.pad(o, ([[0, pad_size]] + [[0, 0] for _ in range(1, len(o.shape))]), constant_values=(- 1)) for o in other_]
    boxes.set_shape([max_detections, 4])
    scores.set_shape([max_detections])
    labels.set_shape([max_detections])
    for (o, s) in zip(other_, [list(tf.keras.backend.int_shape(o)) for o in other]):
        o.set_shape(([max_detections] + s[1:]))
    return ([boxes, scores, labels] + other_)
