import utils
import tensorflow as tf
import logging


def build_graph(self, x):
    (output, attention_feature_map) = self.self_attention_autoencoder(x)
    output = utils.batch_mean_image_subtraction(output)
    summaries = set(tf.get_collection(tf.GraphKeys.SUMMARIES))
    if (self.recons_weight > 0.0):
        recons_loss = tf.losses.mean_squared_error(x, output, weights=self.recons_weight, scope='recons_loss')
        self.recons_loss = recons_loss
        self.total_loss += recons_loss
        summaries.add(tf.summary.scalar('losses/recons_loss', recons_loss))
    if (self.perceptual_weight > 0.0):
        input_features = utils.extract_image_features(x, True)
        output_features = utils.extract_image_features(output, True)
        perceptual_loss = 0.0
        for layer in self.perceptual_loss_layers:
            input_perceptual_features = input_features[('vgg_19/' + layer)]
            output_perceptual_features = output_features[('vgg_19/' + layer)]
            perceptual_loss += tf.losses.mean_squared_error(input_perceptual_features, output_perceptual_features, weights=self.perceptual_weight, scope=layer)
        self.perceptual_loss = perceptual_loss
        self.total_loss += perceptual_loss
        summaries.add(tf.summary.scalar('losses/perceptual_loss', perceptual_loss))
    if (self.tv_weight > 0.0):
        tv_loss = utils.compute_total_variation_loss_l1(output, self.tv_weight)
        self.tv_loss = tv_loss
        self.total_loss += tv_loss
        summaries.add(tf.summary.scalar('losses/tv_loss', tv_loss))
    if (self.attention_weight > 0.0):
        atten_l1_loss = (self.attention_weight * tf.norm(attention_feature_map, 1))
        self.attention_l1_loss = atten_l1_loss
        self.total_loss += atten_l1_loss
        summaries.add(tf.summary.scalar('losses/attention_l1_loss', atten_l1_loss))
    summaries.add(tf.summary.scalar('losses/total_loss', self.total_loss))
    image_tiles = tf.concat([x, output], axis=2)
    image_tiles = utils.batch_mean_image_summation(image_tiles)
    image_tiles = tf.cast(tf.clip_by_value(image_tiles, 0.0, 255.0), tf.uint8)
    summaries.add(tf.summary.image('image_comparison', image_tiles, max_outputs=8))
    self.summaries = summaries
    return self.total_loss
