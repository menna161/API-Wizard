from .builder import build_unet
from ..utils import freeze_model
from ..backbones import get_backbone


def Unet(backbone_name='vgg16', input_shape=(None, None, 3), input_tensor=None, encoder_weights='imagenet', freeze_encoder=False, skip_connections='default', decoder_block_type='upsampling', decoder_filters=(256, 128, 64, 32, 16), decoder_use_batchnorm=False, n_upsample_blocks=5, upsample_rates=(2, 2, 2, 2, 2), classes=1, activation='sigmoid'):
    "\n\n    Args:\n        backbone_name: (str) look at list of available backbones.\n        input_shape:  (tuple) dimensions of input data (H, W, C)\n        input_tensor: keras tensor\n        encoder_weights: one of `None` (random initialization), 'imagenet' (pre-training on ImageNet)\n        freeze_encoder: (bool) Set encoder layers weights as non-trainable. Useful for fine-tuning\n        skip_connections: if 'default' is used take default skip connections,\n            else provide a list of layer numbers or names starting from top of model\n        decoder_block_type: (str) one of 'upsampling' and 'transpose' (look at blocks.py)\n        decoder_filters: (int) number of convolution filters in last upsample block\n        decoder_use_batchnorm: (bool) if True add batch normalisation layer between `Conv2D` ad `Activation` layers\n        n_upsample_blocks: (int) a number of upsampling blocks\n        upsample_rates: (tuple of int) upsampling rates decoder blocks\n        classes: (int) a number of classes for output\n        activation: (str) one of keras activations\n\n    Returns:\n        keras.models.Model instance\n\n    "
    backbone = get_backbone(backbone_name, input_shape=input_shape, input_tensor=input_tensor, weights=encoder_weights, include_top=False)
    if (skip_connections == 'default'):
        skip_connections = DEFAULT_SKIP_CONNECTIONS[backbone_name]
    model = build_unet(backbone, classes, skip_connections, decoder_filters=decoder_filters, block_type=decoder_block_type, activation=activation, n_upsample_blocks=n_upsample_blocks, upsample_rates=upsample_rates, use_batchnorm=decoder_use_batchnorm)
    if freeze_encoder:
        freeze_model(backbone)
    model.name = 'u-{}'.format(backbone_name)
    return model
