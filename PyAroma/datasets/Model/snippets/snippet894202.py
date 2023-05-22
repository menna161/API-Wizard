from __future__ import print_function
import argparse
import os
import time
from glob import glob
import tensorflow as tf
from tensorflow.python.client import timeline
from wavenet import WaveNetModel
from datasets import DataFeederWavenet
from hparams import hparams
from utils import validate_directories, load, save, infolog


def main():

    def _str_to_bool(s):
        'Convert string to bool (in argparse context).'
        if (s.lower() not in ['true', 'false']):
            raise ValueError('Argument needs to be a boolean, got {}'.format(s))
        return {'true': True, 'false': False}[s.lower()]
    parser = argparse.ArgumentParser(description='WaveNet example network')
    DATA_DIRECTORY = '.\\data\\moon,.\\data\\son'
    parser.add_argument('--data_dir', type=str, default=DATA_DIRECTORY, help='The directory containing the VCTK corpus.')
    LOGDIR = None
    parser.add_argument('--logdir', type=str, default=LOGDIR, help='Directory in which to store the logging information for TensorBoard. If the model already exists, it will restore the state and will continue training. Cannot use with --logdir_root and --restore_from.')
    parser.add_argument('--logdir_root', type=str, default=None, help='Root directory to place the logging output and generated model. These are stored under the dated subdirectory of --logdir_root. Cannot use with --logdir.')
    parser.add_argument('--restore_from', type=str, default=None, help='Directory in which to restore the model from. This creates the new model under the dated directory in --logdir_root. Cannot use with --logdir.')
    CHECKPOINT_EVERY = 1000
    parser.add_argument('--checkpoint_every', type=int, default=CHECKPOINT_EVERY, help=(('How many steps to save each checkpoint after. Default: ' + str(CHECKPOINT_EVERY)) + '.'))
    config = parser.parse_args()
    config.data_dir = config.data_dir.split(',')
    try:
        directories = validate_directories(config, hparams)
    except ValueError as e:
        print('Some arguments are wrong:')
        print(str(e))
        return
    logdir = directories['logdir']
    restore_from = directories['restore_from']
    is_overwritten_training = (logdir != restore_from)
    log_path = os.path.join(logdir, 'train.log')
    infolog.init(log_path, logdir)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    coord = tf.train.Coordinator()
    num_speakers = len(config.data_dir)
    with tf.name_scope('create_inputs'):
        silence_threshold = (hparams.silence_threshold if (hparams.silence_threshold > EPSILON) else None)
        gc_enable = (num_speakers > 1)
        reader = DataFeederWavenet(coord, config.data_dir, batch_size=hparams.wavenet_batch_size, receptive_field=WaveNetModel.calculate_receptive_field(hparams.filter_width, hparams.dilations, hparams.scalar_input, hparams.initial_filter_width), gc_enable=gc_enable)
        if gc_enable:
            (audio_batch, lc_batch, gc_id_batch) = (reader.inputs_wav, reader.local_condition, reader.speaker_id)
        else:
            (audio_batch, lc_batch) = (reader.inputs_wav, self.local_condition)
    net = WaveNetModel(batch_size=hparams.wavenet_batch_size, dilations=hparams.dilations, filter_width=hparams.filter_width, residual_channels=hparams.residual_channels, dilation_channels=hparams.dilation_channels, quantization_channels=hparams.quantization_channels, out_channels=hparams.out_channels, skip_channels=hparams.skip_channels, use_biases=hparams.use_biases, scalar_input=hparams.scalar_input, initial_filter_width=hparams.initial_filter_width, global_condition_channels=hparams.gc_channels, global_condition_cardinality=num_speakers, local_condition_channels=hparams.num_mels, upsample_factor=hparams.upsample_factor, train_mode=True)
    if (hparams.l2_regularization_strength == 0):
        hparams.l2_regularization_strength = None
    net.add_loss(input_batch=audio_batch, local_condition=lc_batch, global_condition_batch=gc_id_batch, l2_regularization_strength=hparams.l2_regularization_strength)
    net.add_optimizer(hparams, global_step)
    run_metadata = tf.RunMetadata()
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
    init = tf.global_variables_initializer()
    sess.run(init)
    saver = tf.train.Saver(var_list=tf.global_variables(), max_to_keep=hparams.max_checkpoints)
    try:
        start_step = load(saver, sess, restore_from)
        if (is_overwritten_training or (start_step is None)):
            zero_step_assign = tf.assign(global_step, 0)
            sess.run(zero_step_assign)
    except:
        print('Something went wrong while restoring checkpoint. We will terminate training to avoid accidentally overwriting the previous model.')
        raise
    start_step = sess.run(global_step)
    last_saved_step = start_step
    try:
        reader.start_in_session(sess, start_step)
        while (not coord.should_stop()):
            start_time = time.time()
            if (hparams.store_metadata and ((step % 50) == 0)):
                log('Storing metadata')
                run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                (step, loss_value, _) = sess.run([global_step, net.loss, net.optimize], options=run_options, run_metadata=run_metadata)
                tl = timeline.Timeline(run_metadata.step_stats)
                timeline_path = os.path.join(logdir, 'timeline.trace')
                with open(timeline_path, 'w') as f:
                    f.write(tl.generate_chrome_trace_format(show_memory=True))
            else:
                (step, loss_value, _) = sess.run([global_step, net.loss, net.optimize])
            duration = (time.time() - start_time)
            log('step {:d} - loss = {:.3f}, ({:.3f} sec/step)'.format(step, loss_value, duration))
            if ((step % config.checkpoint_every) == 0):
                save(saver, sess, logdir, step)
                last_saved_step = step
            if (step >= hparams.num_steps):
                raise Exception('End xxx~~~yyy')
    except Exception as e:
        print('finally')
        coord.request_stop(e)
