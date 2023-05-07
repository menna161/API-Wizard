import tensorflow as tf
from net.ops import random_bbox, bbox2mask, local_patch
from net.ops import gan_wgan_loss, gradients_penalty, random_interpolates
from net.ops import free_form_mask_tf
from util.util import f2uint
from functools import partial


def build_net(self, batch_data, config, summary=True, reuse=False):
    self.config = config
    batch_pos = ((batch_data / 127.5) - 1.0)
    if (config.mask_type == 'rect'):
        bbox = random_bbox(config)
        mask = bbox2mask(bbox, config, name='mask_c')
    else:
        mask = free_form_mask_tf(parts=8, im_size=(config.img_shapes[0], config.img_shapes[1]), maxBrushWidth=20, maxLength=80, maxVertex=16)
    batch_incomplete = (batch_pos * (1.0 - mask))
    mask_priority = priority_loss_mask(mask)
    (x_coarse, x_fine, layout, orth_loss) = self.build_generator(batch_incomplete, mask, reuse=reuse)
    losses = {}
    losses['orth_loss'] = orth_loss
    if summary:
        tf.summary.scalar('losses/orth_loss', losses['orth_loss'])
    if (config.pretrain_network is True):
        batch_predicted = x_fine
    else:
        batch_predicted = x_fine
    batch_complete = ((batch_predicted * mask) + (batch_incomplete * (1.0 - mask)))
    if (config.mask_type == 'rect'):
        local_patch_batch_pos = local_patch(batch_pos, bbox)
        local_patch_batch_complete = local_patch(batch_complete, bbox)
        local_patch_mask = local_patch(mask, bbox)
        local_patch_batch_pred = local_patch(batch_predicted, bbox)
        mask_priority = local_patch(mask_priority, bbox)
        local_patch_x_coarse = local_patch(x_coarse, bbox)
        local_patch_x_fine = local_patch(x_fine, bbox)
    else:
        local_patch_batch_pos = batch_pos
        local_patch_batch_complete = batch_complete
        local_patch_batch_pred = batch_predicted
        local_patch_x_coarse = x_coarse
        local_patch_x_fine = x_fine
    if config.pretrain_network:
        print('Pretrain the whole net with only reconstruction loss.')
    ID_MRF_loss = 0
    if ((config.pretrain_network is False) and (config.mrf_alpha != 0)):
        config.feat_style_layers = {'conv3_2': 1.0, 'conv4_2': 1.0}
        config.feat_content_layers = {'conv4_2': 1.0}
        config.mrf_style_w = 1.0
        config.mrf_content_w = 1.0
        ID_MRF_loss = id_mrf_reg(local_patch_batch_pred, local_patch_batch_pos, config)
        losses['ID_MRF_loss'] = ID_MRF_loss
        tf.summary.scalar('losses/ID_MRF_loss', losses['ID_MRF_loss'])
    pretrain_l1_alpha = config.pretrain_l1_alpha
    losses['l1_loss'] = (pretrain_l1_alpha * tf.reduce_mean((tf.abs((local_patch_batch_pos - local_patch_x_coarse)) * mask_priority)))
    if (not config.pretrain_network):
        losses['l1_loss'] += (pretrain_l1_alpha * tf.reduce_mean((tf.abs((local_patch_batch_pos - local_patch_x_fine)) * mask_priority)))
        losses['l1_loss'] += tf.reduce_mean((ID_MRF_loss * config.mrf_alpha))
    losses['ae_loss'] = (pretrain_l1_alpha * tf.reduce_mean((tf.abs((batch_pos - x_coarse)) * (1.0 - mask))))
    if (not config.pretrain_network):
        losses['ae_loss'] += (pretrain_l1_alpha * tf.reduce_mean((tf.abs((batch_pos - x_fine)) * (1.0 - mask))))
    losses['ae_loss'] /= tf.reduce_mean((1.0 - mask))
    if summary:
        viz_img = tf.concat([batch_pos, batch_incomplete, x_coarse, batch_predicted, batch_complete], axis=2)
        tf.summary.image('gt__degraded__coarse-predicted__predicted__completed', f2uint(viz_img))
        tf.summary.scalar('losses/l1_loss', losses['l1_loss'])
        tf.summary.scalar('losses/ae_loss', losses['ae_loss'])
    batch_pos_neg = tf.concat([batch_pos, batch_complete], axis=0)
    if (config.mask_type == 'rect'):
        local_patch_batch_pos_neg = tf.concat([local_patch_batch_pos, local_patch_batch_complete], 0)
        (pos_neg_local, pos_neg_global) = self.wgan_discriminator(local_patch_batch_pos_neg, batch_pos_neg, config.d_cnum, reuse=reuse)
    else:
        (pos_neg_local, pos_neg_global, mask_local) = self.wgan_mask_discriminator(batch_pos_neg, mask, config.d_cnum, reuse=reuse)
    (pos_local, neg_local) = tf.split(pos_neg_local, 2)
    (pos_global, neg_global) = tf.split(pos_neg_global, 2)
    global_wgan_loss_alpha = 1.0
    (g_loss_local, d_loss_local) = gan_wgan_loss(pos_local, neg_local, name='gan/local_gan')
    (g_loss_global, d_loss_global) = gan_wgan_loss(pos_global, neg_global, name='gan/global_gan')
    losses['g_loss'] = ((global_wgan_loss_alpha * g_loss_global) + g_loss_local)
    losses['d_loss'] = (d_loss_global + d_loss_local)
    interpolates_global = random_interpolates(batch_pos, batch_complete)
    if (config.mask_type == 'rect'):
        interpolates_local = random_interpolates(local_patch_batch_pos, local_patch_batch_complete)
        (dout_local, dout_global) = self.wgan_discriminator(interpolates_local, interpolates_global, config.d_cnum, reuse=True)
    else:
        interpolates_local = interpolates_global
        (dout_local, dout_global, _) = self.wgan_mask_discriminator(interpolates_global, mask, config.d_cnum, reuse=True)
    if (config.mask_type == 'rect'):
        penalty_local = gradients_penalty(interpolates_local, dout_local, mask=local_patch_mask)
    else:
        penalty_local = gradients_penalty(interpolates_local, dout_local, mask=mask)
    penalty_global = gradients_penalty(interpolates_global, dout_global, mask=mask)
    losses['gp_loss'] = (config.wgan_gp_lambda * (penalty_local + penalty_global))
    losses['d_loss'] = (losses['d_loss'] + losses['gp_loss'])
    if (summary and (not config.pretrain_network)):
        tf.summary.scalar('convergence/d_loss', losses['d_loss'])
        tf.summary.scalar('convergence/local_d_loss', d_loss_local)
        tf.summary.scalar('convergence/global_d_loss', d_loss_global)
        tf.summary.scalar('gan_wgan_loss/gp_loss', losses['gp_loss'])
        tf.summary.scalar('gan_wgan_loss/gp_penalty_local', penalty_local)
        tf.summary.scalar('gan_wgan_loss/gp_penalty_global', penalty_global)
    if config.pretrain_network:
        losses['g_loss'] = 0
    else:
        losses['g_loss'] = (config.gan_loss_alpha * losses['g_loss'])
        losses['g_loss'] += (config.orth_loss_alpha * losses['orth_loss'])
    losses['g_loss'] += (config.l1_loss_alpha * losses['l1_loss'])
    print(('Set L1_LOSS_ALPHA to %f' % config.l1_loss_alpha))
    print(('Set GAN_LOSS_ALPHA to %f' % config.gan_loss_alpha))
    losses['g_loss'] += (config.ae_loss_alpha * losses['ae_loss'])
    print(('Set AE_LOSS_ALPHA to %f' % config.ae_loss_alpha))
    tf.summary.scalar('losses/g_loss', losses['g_loss'])
    g_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'inpaint_net')
    d_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'discriminator')
    return (g_vars, d_vars, losses)
