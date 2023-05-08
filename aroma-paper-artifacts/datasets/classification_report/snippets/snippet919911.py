from model import net
from argparse import ArgumentParser
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
import numpy as np
from tqdm import tqdm
from helper import showClassTable, maybeExtract, maybeDownloadOrExtract, GroundTruthVisualise


def evaluate(opt):
    (_, _, TEST) = maybeExtract(opt.data, opt.patch_size)
    (test_data, test_label) = (TEST[0], TEST[1])
    HEIGHT = test_data.shape[1]
    WIDTH = test_data.shape[2]
    CHANNELS = test_data.shape[3]
    N_PARALLEL_BAND = number_of_band[opt.data]
    NUM_CLASS = test_label.shape[1]
    graph = tf.Graph()
    with graph.as_default():
        img_entry = tf.placeholder(tf.float32, shape=[None, WIDTH, HEIGHT, CHANNELS])
        img_label = tf.placeholder(tf.uint8, shape=[None, NUM_CLASS])
        image_true_class = tf.argmax(img_label, axis=1)
        prob = tf.placeholder(tf.float32)
        model = net(img_entry, prob, HEIGHT, WIDTH, CHANNELS, N_PARALLEL_BAND, NUM_CLASS)
        final_layer = model['dense3']
        with tf.name_scope('loss'):
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(logits=final_layer, labels=img_label)
            cost = tf.reduce_mean(cross_entropy)
        with tf.name_scope('adam_optimizer'):
            optimizer = tf.train.AdamOptimizer(learning_rate=0.0005).minimize(cost)
        with tf.name_scope('accuracy'):
            predict_class = model['predict_class_number']
            correction = tf.equal(predict_class, image_true_class)
        accuracy = tf.reduce_mean(tf.cast(correction, tf.float32))
        saver = tf.train.Saver()
        with tf.Session(graph=graph) as session:
            saver.restore(session, tf.train.latest_checkpoint((('./Trained_model/' + str(opt.data)) + '/')))

            def test(t_data, t_label, test_iterations=1, evalate=False):
                assert (test_data.shape[0] == test_label.shape[0])
                y_predict_class = model['predict_class_number']
                (overAllAcc, avgAcc, averageAccClass) = ([], [], [])
                for _ in range(test_iterations):
                    pred_class = []
                    for t in tqdm(t_data):
                        t = np.expand_dims(t, axis=0)
                        feed_dict_test = {img_entry: t, prob: 1.0}
                        prediction = session.run(y_predict_class, feed_dict=feed_dict_test)
                        pred_class.append(prediction)
                    true_class = np.argmax(t_label, axis=1)
                    conMatrix = confusion_matrix(true_class, pred_class)
                    classArray = []
                    for c in range(len(conMatrix)):
                        recallScore = (conMatrix[c][c] / sum(conMatrix[c]))
                        classArray += [recallScore]
                    averageAccClass.append(classArray)
                    avgAcc.append((sum(classArray) / len(classArray)))
                    overAllAcc.append(accuracy_score(true_class, pred_class))
                averageAccClass = np.transpose(averageAccClass)
                meanPerClass = np.mean(averageAccClass, axis=1)
                showClassTable(meanPerClass, title='Class accuracy')
                print(('Average Accuracy: ' + str(np.mean(avgAcc))))
                print(('Overall Accuracy: ' + str(np.mean(overAllAcc))))

            def pixelClassification():
                (input_mat, _) = maybeDownloadOrExtract(opt.data)
                (input_height, input_width) = (input_mat.shape[0], input_mat.shape[1])
                BAND = input_mat.shape[2]
                PATCH_SIZE = opt.patch_size
                MEAN_ARRAY = np.ndarray(shape=(BAND, 1))
                new_input_mat = []
                calib_val_pad = int(((PATCH_SIZE - 1) / 2))
                for i in range(BAND):
                    MEAN_ARRAY[i] = np.mean(input_mat[(:, :, i)])
                    new_input_mat.append(np.pad(input_mat[(:, :, i)], calib_val_pad, 'constant', constant_values=0))
                new_input_mat = np.transpose(new_input_mat, (1, 2, 0))
                input_mat = new_input_mat

                def Patch(height_index, width_index):
                    transpose_array = input_mat
                    height_slice = slice(height_index, (height_index + PATCH_SIZE))
                    width_slice = slice(width_index, (width_index + PATCH_SIZE))
                    patch = transpose_array[(height_slice, width_slice, :)]
                    mean_normalized_patch = []
                    for i in range(BAND):
                        mean_normalized_patch.append((patch[(:, :, i)] - MEAN_ARRAY[i]))
                    mean_normalized_patch = np.array(mean_normalized_patch).astype(np.float16)
                    mean_normalized_patch = np.transpose(mean_normalized_patch, (1, 2, 0))
                    return mean_normalized_patch
                labelled_img = np.ndarray(shape=(input_height, input_width))
                for i in tqdm(range((input_height - 1))):
                    for j in range((input_width - 1)):
                        current_input = Patch(i, j)
                        current_input = np.expand_dims(current_input, axis=0)
                        feed_dict_test = {img_entry: current_input, prob: 1.0}
                        prediction = session.run(model['predict_class_number'], feed_dict=feed_dict_test)
                        labelled_img[(i, j)] = prediction[0]
                labelled_img += 1
                labelled_img = np.pad(labelled_img, [(0, 1), (0, 0)], 'constant', constant_values=(0, 0))
                print(np.min(labelled_img), np.max(labelled_img), labelled_img.shape)
                GroundTruthVisualise(labelled_img, opt.data, False)
            test(test_data, test_label, test_iterations=1)
            pixelClassification()
