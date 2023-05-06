from ops import *
from utils import *
import time
from tensorflow.contrib.data import prefetch_to_device, shuffle_and_repeat, map_and_batch
import numpy as np
from glob import glob
from tqdm import tqdm


def build_model(self):
    self.ema = tf.train.ExponentialMovingAverage(decay=self.ema_decay)
    if (self.phase == 'train'):
        ' Input Image'
        img_class = Image_data(self.img_height, self.img_width, self.img_ch, self.dataset_path, self.label_list, self.augment_flag)
        img_class.preprocess()
        dataset_num = len(img_class.image)
        print('Dataset number : ', dataset_num)
        self.lr = tf.placeholder(tf.float32, name='learning_rate')
        self.ds_weight_placeholder = tf.placeholder(tf.float32, name='ds_weight')
        img_and_label = tf.data.Dataset.from_tensor_slices((img_class.image, img_class.label))
        gpu_device = '/gpu:0'
        img_and_label = img_and_label.apply(shuffle_and_repeat(dataset_num)).apply(map_and_batch(img_class.image_processing, (self.batch_size * self.gpu_num), num_parallel_batches=16, drop_remainder=True)).apply(prefetch_to_device(gpu_device, None))
        img_and_label_iterator = img_and_label.make_one_shot_iterator()
        (self.x_real, label_org) = img_and_label_iterator.get_next()
        label_trg = tf.random_uniform(shape=tf.shape(label_org), minval=0, maxval=self.c_dim, dtype=tf.int32)
        ' split '
        x_real_gpu_split = tf.split(self.x_real, num_or_size_splits=self.gpu_num, axis=0)
        label_org_gpu_split = tf.split(label_org, num_or_size_splits=self.gpu_num, axis=0)
        label_trg_gpu_split = tf.split(label_trg, num_or_size_splits=self.gpu_num, axis=0)
        g_adv_loss_per_gpu = []
        g_sty_recon_loss_per_gpu = []
        g_sty_diverse_loss_per_gpu = []
        g_cyc_loss_per_gpu = []
        g_loss_per_gpu = []
        d_adv_loss_per_gpu = []
        d_loss_per_gpu = []
        for gpu_id in range(self.gpu_num):
            with tf.device(tf.DeviceSpec(device_type='GPU', device_index=gpu_id)):
                with tf.variable_scope(tf.get_variable_scope(), reuse=(gpu_id > 0)):
                    x_real_split = tf.split(x_real_gpu_split[gpu_id], num_or_size_splits=self.batch_size, axis=0)
                    label_org_split = tf.split(label_org_gpu_split[gpu_id], num_or_size_splits=self.batch_size, axis=0)
                    label_trg_split = tf.split(label_trg_gpu_split[gpu_id], num_or_size_splits=self.batch_size, axis=0)
                    g_adv_loss = None
                    g_sty_recon_loss = None
                    g_sty_diverse_loss = None
                    g_cyc_loss = None
                    d_adv_loss = None
                    d_simple_gp = None
                    d_gp = None
                    for each_bs in range(self.batch_size):
                        ' Define Generator, Discriminator '
                        x_real_each = x_real_split[each_bs]
                        label_org_each = tf.squeeze(label_org_split[each_bs], axis=[0, 1])
                        label_trg_each = tf.squeeze(label_trg_split[each_bs], axis=[0, 1])
                        random_style_code = tf.random_normal(shape=[1, self.style_dim])
                        random_style_code_1 = tf.random_normal(shape=[1, self.style_dim])
                        random_style_code_2 = tf.random_normal(shape=[1, self.style_dim])
                        random_style = tf.gather(self.mapping_network(random_style_code), label_trg_each)
                        random_style_1 = tf.gather(self.mapping_network(random_style_code_1), label_trg_each)
                        random_style_2 = tf.gather(self.mapping_network(random_style_code_2), label_trg_each)
                        x_fake = self.generator(x_real_each, random_style)
                        x_fake_1 = self.generator(x_real_each, random_style_1)
                        x_fake_2 = self.generator(x_real_each, random_style_2)
                        x_real_each_style = tf.gather(self.style_encoder(x_real_each), label_org_each)
                        x_fake_style = tf.gather(self.style_encoder(x_fake), label_trg_each)
                        x_cycle = self.generator(x_fake, x_real_each_style)
                        real_logit = tf.gather(self.discriminator(x_real_each), label_org_each)
                        fake_logit = tf.gather(self.discriminator(x_fake), label_trg_each)
                        ' Define loss '
                        if (self.gan_type.__contains__('wgan') or (self.gan_type == 'dragan')):
                            GP = self.gradient_panalty(real=x_real_each, fake=x_fake, real_label=label_org_each)
                        else:
                            GP = tf.constant([0], tf.float32)
                        if (each_bs == 0):
                            g_adv_loss = (self.adv_weight * generator_loss(self.gan_type, fake_logit))
                            g_sty_recon_loss = (self.sty_weight * L1_loss(random_style, x_fake_style))
                            g_sty_diverse_loss = (self.ds_weight_placeholder * L1_loss(x_fake_1, x_fake_2))
                            g_cyc_loss = (self.cyc_weight * L1_loss(x_real_each, x_cycle))
                            d_adv_loss = (self.adv_weight * discriminator_loss(self.gan_type, real_logit, fake_logit))
                            d_simple_gp = (self.adv_weight * simple_gp(real_logit, fake_logit, x_real_each, x_fake, r1_gamma=self.r1_weight, r2_gamma=0.0))
                            d_gp = (self.adv_weight * GP)
                        else:
                            g_adv_loss = tf.concat([g_adv_loss, (self.adv_weight * generator_loss(self.gan_type, fake_logit))], axis=0)
                            g_sty_recon_loss = tf.concat([g_sty_recon_loss, (self.sty_weight * L1_loss(random_style, x_fake_style))], axis=0)
                            g_sty_diverse_loss = tf.concat([g_sty_diverse_loss, (self.ds_weight_placeholder * L1_loss(x_fake_1, x_fake_2))], axis=0)
                            g_cyc_loss = tf.concat([g_cyc_loss, (self.cyc_weight * L1_loss(x_real_each, x_cycle))], axis=0)
                            d_adv_loss = tf.concat([d_adv_loss, (self.adv_weight * discriminator_loss(self.gan_type, real_logit, fake_logit))], axis=0)
                            d_simple_gp = tf.concat([d_simple_gp, (self.adv_weight * simple_gp(real_logit, fake_logit, x_real_each, x_fake, r1_gamma=self.r1_weight, r2_gamma=0.0))], axis=0)
                            d_gp = tf.concat([d_gp, (self.adv_weight * GP)], axis=0)
                    g_adv_loss = tf.reduce_mean(g_adv_loss)
                    g_sty_recon_loss = tf.reduce_mean(g_sty_recon_loss)
                    g_sty_diverse_loss = tf.reduce_mean(g_sty_diverse_loss)
                    g_cyc_loss = tf.reduce_mean(g_cyc_loss)
                    d_adv_loss = tf.reduce_mean(d_adv_loss)
                    d_simple_gp = tf.reduce_mean(tf.reduce_sum(d_simple_gp, axis=[1, 2, 3]))
                    d_gp = tf.reduce_mean(d_gp)
                    g_loss = (((g_adv_loss + g_sty_recon_loss) - g_sty_diverse_loss) + g_cyc_loss)
                    d_loss = ((d_adv_loss + d_simple_gp) + d_gp)
                    g_adv_loss_per_gpu.append(g_adv_loss)
                    g_sty_recon_loss_per_gpu.append(g_sty_recon_loss)
                    g_sty_diverse_loss_per_gpu.append(g_sty_diverse_loss)
                    g_cyc_loss_per_gpu.append(g_cyc_loss)
                    d_adv_loss_per_gpu.append(d_adv_loss)
                    g_loss_per_gpu.append(g_loss)
                    d_loss_per_gpu.append(d_loss)
        g_adv_loss = tf.reduce_mean(g_adv_loss_per_gpu)
        g_sty_recon_loss = tf.reduce_mean(g_sty_recon_loss_per_gpu)
        g_sty_diverse_loss = tf.reduce_mean(g_sty_diverse_loss_per_gpu)
        g_cyc_loss = tf.reduce_mean(g_cyc_loss_per_gpu)
        self.g_loss = tf.reduce_mean(g_loss_per_gpu)
        d_adv_loss = tf.reduce_mean(d_adv_loss_per_gpu)
        self.d_loss = tf.reduce_mean(d_loss_per_gpu)
        ' Training '
        t_vars = tf.trainable_variables()
        G_vars = [var for var in t_vars if ('generator' in var.name)]
        E_vars = [var for var in t_vars if ('encoder' in var.name)]
        F_vars = [var for var in t_vars if ('mapping' in var.name)]
        D_vars = [var for var in t_vars if ('discriminator' in var.name)]
        if (self.gpu_num == 1):
            prev_g_optimizer = tf.train.AdamOptimizer(self.lr, beta1=0, beta2=0.99).minimize(self.g_loss, var_list=G_vars)
            prev_e_optimizer = tf.train.AdamOptimizer(self.lr, beta1=0, beta2=0.99).minimize(self.g_loss, var_list=E_vars)
            prev_f_optimizer = tf.train.AdamOptimizer((self.lr * 0.01), beta1=0, beta2=0.99).minimize(self.g_loss, var_list=F_vars)
            self.d_optimizer = tf.train.AdamOptimizer(self.lr, beta1=0, beta2=0.99).minimize(self.d_loss, var_list=D_vars)
        else:
            prev_g_optimizer = tf.train.AdamOptimizer(self.lr, beta1=0, beta2=0.99).minimize(self.g_loss, var_list=G_vars, colocate_gradients_with_ops=True)
            prev_e_optimizer = tf.train.AdamOptimizer(self.lr, beta1=0, beta2=0.99).minimize(self.g_loss, var_list=E_vars, colocate_gradients_with_ops=True)
            prev_f_optimizer = tf.train.AdamOptimizer((self.lr * 0.01), beta1=0, beta2=0.99).minimize(self.g_loss, var_list=F_vars, colocate_gradients_with_ops=True)
            self.d_optimizer = tf.train.AdamOptimizer(self.lr, beta1=0, beta2=0.99).minimize(self.d_loss, var_list=D_vars, colocate_gradients_with_ops=True)
        with tf.control_dependencies([prev_g_optimizer, prev_e_optimizer, prev_f_optimizer]):
            self.g_optimizer = self.ema.apply(G_vars)
            self.e_optimizer = self.ema.apply(E_vars)
            self.f_optimizer = self.ema.apply(F_vars)
        '" Summary '
        self.Generator_loss = tf.summary.scalar('g_loss', self.g_loss)
        self.Discriminator_loss = tf.summary.scalar('d_loss', self.d_loss)
        self.g_adv_loss = tf.summary.scalar('g_adv_loss', g_adv_loss)
        self.g_sty_recon_loss = tf.summary.scalar('g_sty_recon_loss', g_sty_recon_loss)
        self.g_sty_diverse_loss = tf.summary.scalar('g_sty_diverse_loss', g_sty_diverse_loss)
        self.g_cyc_loss = tf.summary.scalar('g_cyc_loss', g_cyc_loss)
        self.d_adv_loss = tf.summary.scalar('d_adv_loss', d_adv_loss)
        g_summary_list = [self.Generator_loss, self.g_adv_loss, self.g_sty_recon_loss, self.g_sty_diverse_loss, self.g_cyc_loss]
        d_summary_list = [self.Discriminator_loss, self.d_adv_loss]
        self.g_summary_loss = tf.summary.merge(g_summary_list)
        self.d_summary_loss = tf.summary.merge(d_summary_list)
        ' Result Image '

        def return_g_images(generator, image, code):
            x = generator(image, code)
            return x
        self.x_fake_list = []
        first_x_real = tf.expand_dims(self.x_real[0], axis=0)
        label_fix_list = tf.constant([idx for idx in range(self.c_dim)])
        for _ in range(self.num_style):
            random_style_code = tf.truncated_normal(shape=[1, self.style_dim])
            self.x_fake_list.append(tf.map_fn((lambda c: return_g_images(self.generator, first_x_real, tf.gather(self.mapping_network(random_style_code), c))), label_fix_list, dtype=tf.float32))
    elif (self.phase == 'refer_test'):
        ' Test '

        def return_g_images(generator, image, code):
            x = generator(image, code)
            return x
        self.custom_image = tf.placeholder(tf.float32, [1, self.img_height, self.img_width, self.img_ch], name='custom_image')
        self.refer_image = tf.placeholder(tf.float32, [1, self.img_height, self.img_width, self.img_ch], name='refer_image')
        label_fix_list = tf.constant([idx for idx in range(self.c_dim)])
        self.refer_fake_image = tf.map_fn((lambda c: return_g_images(self.generator, self.custom_image, tf.gather(self.style_encoder(self.refer_image), c))), label_fix_list, dtype=tf.float32)
    else:
        ' Test '

        def return_g_images(generator, image, code):
            x = generator(image, code)
            return x
        self.custom_image = tf.placeholder(tf.float32, [1, self.img_height, self.img_width, self.img_ch], name='custom_image')
        label_fix_list = tf.constant([idx for idx in range(self.c_dim)])
        random_style_code = tf.truncated_normal(shape=[1, self.style_dim])
        self.custom_fake_image = tf.map_fn((lambda c: return_g_images(self.generator, self.custom_image, tf.gather(self.mapping_network(random_style_code), c))), label_fix_list, dtype=tf.float32)
