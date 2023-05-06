import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def call(self, Z, debug=False):
    batch_size = Z.shape[0]
    if CFG['JUST_VISION']:
        x = self.init_Z_embed(Z)
    else:
        x = Z
    x = x[(:, tf.newaxis, tf.newaxis)]
    if debug:
        tf.print('GENERATOR')
    if debug:
        tf.print(x.shape)
    for (li, _) in enumerate(self.Z_embeds):
        if debug:
            tf.print(x.shape)
        Z_embeds = self.Z_embeds[li]
        Z_norms = self.Z_norms[li]
        residual_block_1 = self.residual_blocks_1[li]
        residual_block_2 = self.residual_blocks_2[li]
        upsample = self.upsamples[li]
        cond_conv = self.cond_convs[li]
        res_prep = self.res_preps[li]
        x = upsample(x)
        x = res_prep(x)
        x = residual_block_1(x)
        (y_dim, x_dim) = (x.shape[1], x.shape[2])
        loc = generate_scaled_coordinate_hints(batch_size, y_dim, x_dim)
        _z = Z
        for (Z_embed, Z_norm) in zip(Z_embeds, Z_norms):
            _z = Z_embed(_z)
            _z = tf.nn.swish(_z)
            if debug:
                tf.print(f'Z shape: {_z.shape}')
        _z = tf.tile(_z[(:, tf.newaxis, tf.newaxis)], [1, y_dim, x_dim, 1])
        if debug:
            tf.print(f'loc: {loc.shape}, z: {_z.shape}')
        x = tf.concat([x, loc, _z], axis=(- 1))
        if debug:
            tf.print(f'joined shape: {x.shape}')
        x = cond_conv(x)
        x = residual_block_2(x)
    if debug:
        tf.print(x.shape)
    x = self.out_conv(x)
    x = tf.nn.softmax(x, axis=(- 1))
    x = ((x * 2.0) - 1.0)
    if (x.shape[(- 1)] == 1):
        x = tf.tile(x, [1, 1, 1, 3])
    return x
