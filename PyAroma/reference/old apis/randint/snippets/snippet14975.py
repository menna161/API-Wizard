import tensorflow as tf
import numpy as np
import datetime
import os
import argparse
import matplotlib.pyplot as plt
from matplotlib import gridspec
from tensorflow.examples.tutorials.mnist import input_data


def train(train_model=True):
    '\n    Used to train the autoencoder by passing in the necessary inputs.\n    :param train_model: True -> Train the model, False -> Load the latest trained model and show the image grid.\n    :return: does not return anything\n    '
    with tf.variable_scope(tf.get_variable_scope()):
        (encoder_output_label, encoder_output_latent) = encoder(x_input)
        decoder_input = tf.concat([encoder_output_label, encoder_output_latent], 1)
        decoder_output = decoder(decoder_input)
    with tf.variable_scope(tf.get_variable_scope()):
        d_g_real = discriminator_gauss(real_distribution)
        d_g_fake = discriminator_gauss(encoder_output_latent, reuse=True)
    with tf.variable_scope(tf.get_variable_scope()):
        d_c_real = discriminator_categorical(categorial_distribution)
        d_c_fake = discriminator_categorical(encoder_output_label, reuse=True)
    with tf.variable_scope(tf.get_variable_scope()):
        (encoder_output_label_, _) = encoder(x_input_l, reuse=True, supervised=True)
    with tf.variable_scope(tf.get_variable_scope()):
        decoder_image = decoder(manual_decoder_input, reuse=True)
    correct_pred = tf.equal(tf.argmax(encoder_output_label_, 1), tf.argmax(y_input, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    autoencoder_loss = tf.reduce_mean(tf.square((x_target - decoder_output)))
    dc_g_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.ones_like(d_g_real), logits=d_g_real))
    dc_g_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.zeros_like(d_g_fake), logits=d_g_fake))
    dc_g_loss = (dc_g_loss_fake + dc_g_loss_real)
    dc_c_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.ones_like(d_c_real), logits=d_c_real))
    dc_c_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.zeros_like(d_c_fake), logits=d_c_fake))
    dc_c_loss = (dc_c_loss_fake + dc_c_loss_real)
    generator_g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.ones_like(d_g_fake), logits=d_g_fake))
    generator_c_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.ones_like(d_c_fake), logits=d_c_fake))
    generator_loss = (generator_c_loss + generator_g_loss)
    supervised_encoder_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_input, logits=encoder_output_label_))
    all_variables = tf.trainable_variables()
    dc_g_var = [var for var in all_variables if ('dc_g_' in var.name)]
    dc_c_var = [var for var in all_variables if ('dc_c_' in var.name)]
    en_var = [var for var in all_variables if ('e_' in var.name)]
    autoencoder_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=beta1).minimize(autoencoder_loss)
    discriminator_g_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=beta1).minimize(dc_g_loss, var_list=dc_g_var)
    discriminator_c_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=beta1).minimize(dc_c_loss, var_list=dc_c_var)
    generator_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=beta1).minimize(generator_loss, var_list=en_var)
    supervised_encoder_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate, beta1=beta1).minimize(supervised_encoder_loss, var_list=en_var)
    init = tf.global_variables_initializer()
    input_images = tf.reshape(x_input, [(- 1), 28, 28, 1])
    generated_images = tf.reshape(decoder_output, [(- 1), 28, 28, 1])
    tf.summary.scalar(name='Autoencoder Loss', tensor=autoencoder_loss)
    tf.summary.scalar(name='Discriminator gauss Loss', tensor=dc_g_loss)
    tf.summary.scalar(name='Discriminator categorical Loss', tensor=dc_c_loss)
    tf.summary.scalar(name='Generator Loss', tensor=generator_loss)
    tf.summary.scalar(name='Supervised Encoder Loss', tensor=supervised_encoder_loss)
    tf.summary.histogram(name='Encoder Gauss Distribution', values=encoder_output_latent)
    tf.summary.histogram(name='Real Gauss Distribution', values=real_distribution)
    tf.summary.histogram(name='Encoder Categorical Distribution', values=encoder_output_label)
    tf.summary.histogram(name='Real Categorical Distribution', values=categorial_distribution)
    tf.summary.image(name='Input Images', tensor=input_images, max_outputs=10)
    tf.summary.image(name='Generated Images', tensor=generated_images, max_outputs=10)
    summary_op = tf.summary.merge_all()
    saver = tf.train.Saver()
    step = 0
    with tf.Session() as sess:
        if train_model:
            (tensorboard_path, saved_model_path, log_path) = form_results()
            sess.run(init)
            writer = tf.summary.FileWriter(logdir=tensorboard_path, graph=sess.graph)
            (x_l, y_l) = mnist.test.next_batch(n_labeled)
            for i in range(n_epochs):
                n_batches = int((n_labeled / batch_size))
                print('------------------Epoch {}/{}------------------'.format(i, n_epochs))
                for b in range(1, (n_batches + 1)):
                    z_real_dist = (np.random.randn(batch_size, z_dim) * 5.0)
                    real_cat_dist = np.random.randint(low=0, high=10, size=batch_size)
                    real_cat_dist = np.eye(n_labels)[real_cat_dist]
                    (batch_x_ul, _) = mnist.train.next_batch(batch_size)
                    (batch_x_l, batch_y_l) = next_batch(x_l, y_l, batch_size=batch_size)
                    sess.run(autoencoder_optimizer, feed_dict={x_input: batch_x_ul, x_target: batch_x_ul})
                    sess.run(discriminator_g_optimizer, feed_dict={x_input: batch_x_ul, x_target: batch_x_ul, real_distribution: z_real_dist})
                    sess.run(discriminator_c_optimizer, feed_dict={x_input: batch_x_ul, x_target: batch_x_ul, categorial_distribution: real_cat_dist})
                    sess.run(generator_optimizer, feed_dict={x_input: batch_x_ul, x_target: batch_x_ul})
                    sess.run(supervised_encoder_optimizer, feed_dict={x_input_l: batch_x_l, y_input: batch_y_l})
                    if ((b % 5) == 0):
                        (a_loss, d_g_loss, d_c_loss, g_loss, s_loss, summary) = sess.run([autoencoder_loss, dc_g_loss, dc_c_loss, generator_loss, supervised_encoder_loss, summary_op], feed_dict={x_input: batch_x_ul, x_target: batch_x_ul, real_distribution: z_real_dist, y_input: batch_y_l, x_input_l: batch_x_l, categorial_distribution: real_cat_dist})
                        writer.add_summary(summary, global_step=step)
                        print('Epoch: {}, iteration: {}'.format(i, b))
                        print('Autoencoder Loss: {}'.format(a_loss))
                        print('Discriminator Gauss Loss: {}'.format(d_g_loss))
                        print('Discriminator Categorical Loss: {}'.format(d_c_loss))
                        print('Generator Loss: {}'.format(g_loss))
                        print('Supervised Loss: {}\n'.format(s_loss))
                        with open((log_path + '/log.txt'), 'a') as log:
                            log.write('Epoch: {}, iteration: {}\n'.format(i, b))
                            log.write('Autoencoder Loss: {}\n'.format(a_loss))
                            log.write('Discriminator Gauss Loss: {}'.format(d_g_loss))
                            log.write('Discriminator Categorical Loss: {}'.format(d_c_loss))
                            log.write('Generator Loss: {}\n'.format(g_loss))
                            log.write('Supervised Loss: {}'.format(s_loss))
                    step += 1
                acc = 0
                num_batches = int((mnist.validation.num_examples / batch_size))
                for j in range(num_batches):
                    (batch_x_l, batch_y_l) = mnist.validation.next_batch(batch_size=batch_size)
                    encoder_acc = sess.run(accuracy, feed_dict={x_input_l: batch_x_l, y_input: batch_y_l})
                    acc += encoder_acc
                acc /= num_batches
                print('Encoder Classification Accuracy: {}'.format(acc))
                with open((log_path + '/log.txt'), 'a') as log:
                    log.write('Encoder Classification Accuracy: {}'.format(acc))
                saver.save(sess, save_path=saved_model_path, global_step=step)
        else:
            all_results = os.listdir(results_path)
            all_results.sort()
            saver.restore(sess, save_path=tf.train.latest_checkpoint((((results_path + '/') + all_results[(- 1)]) + '/Saved_models/')))
            generate_image_grid(sess, op=decoder_image)
