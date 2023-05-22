from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import numpy as np
import argparse
import json
import glob
import random
import collections
import math
import time
from lxml import etree
from random import shuffle


def main():
    if (a.seed is None):
        a.seed = random.randint(0, ((2 ** 31) - 1))
    tf.set_random_seed(a.seed)
    np.random.seed(a.seed)
    random.seed(a.seed)
    if (not os.path.exists(a.output_dir)):
        os.makedirs(a.output_dir)
    if ((a.mode == 'test') or (a.mode == 'export') or (a.mode == 'eval')):
        if (a.checkpoint is None):
            raise Exception('checkpoint required for test, export or eval mode')
        options = {'which_direction', 'ngf', 'ndf', 'nbTargets', 'depthFactor', 'loss', 'useLog'}
        with open(os.path.join(a.checkpoint, 'options.json')) as f:
            for (key, val) in json.loads(f.read()).items():
                if (key in options):
                    print('loaded', key, '=', val)
                    setattr(a, key, val)
        a.scale_size = CROP_SIZE
        a.flip = False
    for (k, v) in a._get_kwargs():
        print(k, '=', v)
    with open(os.path.join(a.output_dir, 'options.json'), 'w') as f:
        f.write(json.dumps(vars(a), sort_keys=True, indent=4))
    examples = load_examples(a.input_dir, (a.mode == 'train'))
    print((a.mode + (' set count = %d' % examples.count)))
    if (a.mode == 'train'):
        evalExamples = load_examples((a.input_dir.rsplit('/', 1)[0] + '/testBlended'), False)
        print(('evaluation set count = %d' % evalExamples.count))
    model = create_model(examples.inputs, examples.targets, False)
    if (a.mode == 'train'):
        model_test = create_model(evalExamples.inputs, evalExamples.targets, True)
    tmpTargets = examples.targets
    if (a.mode == 'train'):
        tmpTargetsTest = evalExamples.targets
    inputs = deprocess(examples.inputs)
    targets = deprocess(tmpTargets)
    outputs = deprocess(model.outputs)
    if (a.mode == 'train'):
        inputsTests = deprocess(evalExamples.inputs)
        targetsTests = deprocess(tmpTargetsTest)
        outputsTests = deprocess(model_test.outputs)

    def convert(image, squeeze=False):
        if (a.aspect_ratio != 1.0):
            size = [CROP_SIZE, int(round((CROP_SIZE * a.aspect_ratio)))]
            image = tf.image.resize_images(image, size=size, method=tf.image.ResizeMethod.BICUBIC)
        if squeeze:

            def tempLog(imageValue):
                imageValue = tf.log((imageValue + 0.01))
                imageValue = (imageValue - tf.reduce_min(imageValue))
                imageValue = (imageValue / tf.reduce_max(imageValue))
                return imageValue
            image = [tempLog(imageVal) for imageVal in image]
        return tf.image.convert_image_dtype(image, dtype=tf.uint8, saturate=True)
    with tf.name_scope('transform_images'):
        targets_reshaped = reshape_tensor_display(targets, a.nbTargets, logAlbedo=a.logOutputAlbedos)
        outputs_reshaped = reshape_tensor_display(outputs, a.nbTargets, logAlbedo=a.logOutputAlbedos)
        inputs_reshaped = reshape_tensor_display(inputs, 1, logAlbedo=False)
        if (a.mode == 'train'):
            inputs_reshaped_test = reshape_tensor_display(inputsTests, 1, logAlbedo=False)
            targets_test_reshaped = reshape_tensor_display(targetsTests, a.nbTargets, logAlbedo=a.logOutputAlbedos)
            outputs_test_reshaped = reshape_tensor_display(outputsTests, a.nbTargets, logAlbedo=a.logOutputAlbedos)
    with tf.name_scope('convert_inputs'):
        converted_inputs = convert(inputs_reshaped)
        if (a.mode == 'train'):
            converted_inputs_test = convert(inputs_reshaped_test)
    with tf.name_scope('convert_targets'):
        converted_targets = convert(targets_reshaped)
        if (a.mode == 'train'):
            converted_targets_test = convert(targets_test_reshaped)
    with tf.name_scope('convert_outputs'):
        converted_outputs = convert(outputs_reshaped)
        if (a.mode == 'train'):
            converted_outputs_test = convert(outputs_test_reshaped)
    with tf.name_scope('encode_images'):
        display_fetches = {'paths': examples.paths, 'inputs': tf.map_fn(tf.image.encode_png, converted_inputs, dtype=tf.string, name='input_pngs'), 'targets': tf.map_fn(tf.image.encode_png, converted_targets, dtype=tf.string, name='target_pngs'), 'outputs': tf.map_fn(tf.image.encode_png, converted_outputs, dtype=tf.string, name='output_pngs')}
        if (a.mode == 'train'):
            display_fetches_test = {'paths': evalExamples.paths, 'inputs': tf.map_fn(tf.image.encode_png, converted_inputs_test, dtype=tf.string, name='input_pngs'), 'targets': tf.map_fn(tf.image.encode_png, converted_targets_test, dtype=tf.string, name='target_pngs'), 'outputs': tf.map_fn(tf.image.encode_png, converted_outputs_test, dtype=tf.string, name='output_pngs')}
    with tf.name_scope('outputs_summary'):
        tf.summary.image('outputs', converted_outputs, max_outputs=a.nbTargets)
    tf.summary.scalar('generator_loss', model.gen_loss_L1)
    with tf.name_scope('parameter_count'):
        parameter_count = tf.reduce_sum([tf.reduce_prod(tf.shape(v)) for v in tf.trainable_variables()])
    saver = tf.train.Saver(max_to_keep=1)
    logdir = (a.output_dir if (a.summary_freq > 0) else None)
    sv = tf.train.Supervisor(logdir=logdir, save_summaries_secs=0, saver=None)
    with sv.managed_session() as sess:
        print('parameter_count =', sess.run(parameter_count))
        if (a.checkpoint is not None):
            print(('loading model from checkpoint : ' + a.checkpoint))
            checkpoint = tf.train.latest_checkpoint(a.checkpoint)
            saver.restore(sess, checkpoint)
        max_steps = (2 ** 32)
        sess.run(examples.iterator.initializer)
        print('BBBBBBBBbb')
        if ((a.mode == 'test') or (a.mode == 'eval')):
            print('AAAAAAAAAAAAAAA')
            if (a.checkpoint is None):
                print('checkpoint is required for testing')
                return
            print('CCCCCCCCCCCCCCCCc')
            max_steps = min(examples.steps_per_epoch, max_steps)
            print(max_steps)
            for step in range(max_steps):
                try:
                    results = sess.run(display_fetches)
                    filesets = save_images(results)
                    for (i, f) in enumerate(filesets):
                        print('evaluated image', f['name'])
                    index_path = append_index(filesets)
                except tf.errors.OutOfRangeError:
                    print('testing fails in OutOfRangeError')
                    continue
        else:
            try:
                start_time = time.time()
                sess.run(evalExamples.iterator.initializer)
                for step in range(max_steps):

                    def should(freq):
                        return ((freq > 0) and ((((step + 1) % freq) == 0) or (step == (max_steps - 1))))
                    options = None
                    run_metadata = None
                    fetches = {'train': model.train, 'global_step': sv.global_step}
                    if (should(a.progress_freq) or (step == 0) or (step == 1)):
                        fetches['gen_loss_L1'] = model.gen_loss_L1
                    if should(a.summary_freq):
                        fetches['summary'] = sv.summary_op
                    if should(a.display_freq):
                        fetches['display'] = display_fetches
                    try:
                        results = sess.run(fetches, options=options, run_metadata=run_metadata)
                    except tf.errors.OutOfRangeError:
                        print('training fails in OutOfRangeError')
                        continue
                    global_step = results['global_step']
                    if should(a.summary_freq):
                        sv.summary_writer.add_summary(results['summary'], global_step)
                    if should(a.display_freq):
                        print('saving display images')
                        filesets = save_images(results['display'], step=global_step)
                        append_index(filesets, step=True)
                    if should(a.progress_freq):
                        train_epoch = math.ceil((global_step / examples.steps_per_epoch))
                        train_step = (global_step - ((train_epoch - 1) * examples.steps_per_epoch))
                        print(('progress  epoch %d  step %d  image/sec %0.1f' % (train_epoch, train_step, ((global_step * a.batch_size) / (time.time() - start_time)))))
                        print('gen_loss_L1', results['gen_loss_L1'])
                    if should(a.save_freq):
                        print('saving model')
                        saver.save(sess, os.path.join(a.output_dir, 'model'), global_step=sv.global_step)
                    if (should(a.test_freq) or (global_step == 1)):
                        runTestFromTrain(global_step, evalExamples, max_steps, display_fetches_test, sess)
                    if sv.should_stop():
                        break
            finally:
                saver.save(sess, os.path.join(a.output_dir, 'model'), global_step=sv.global_step)
                sess.run(evalExamples.iterator.initializer)
                runTestFromTrain('final', evalExamples, max_steps, display_fetches_test, sess)
