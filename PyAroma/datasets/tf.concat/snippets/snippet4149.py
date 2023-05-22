import tensorflow as tf
from absl import flags
from deepray.base.layers.core import Linear
from deepray.model.model_ctr import BaseCTRModel


def build_features(self, features, embedding_suffix=''):
    '\n        categorical feature id starts from -1 (as missing)\n        '
    if self.flags.wide_cols:
        ev_list = [self.EmbeddingDict[key](features[key]) for key in self.CATEGORY_FEATURES if (key in self.flags.wide_cols)]
        fv_list = [self.build_dense_layer(features[key]) for key in self.NUMERICAL_FEATURES if (key in self.flags.wide_cols)]
        wide_list = self.concat((fv_list + ev_list))
    else:
        ev_list = [self.EmbeddingDict[key](features[key]) for key in self.CATEGORY_FEATURES]
        fv_list = [self.build_dense_layer(features[key]) for key in self.NUMERICAL_FEATURES]
        wide_list = self.concat((fv_list + ev_list))
    if self.flags.deep_cols:
        ev_list = [self.EmbeddingDict[key](features[key]) for key in self.CATEGORY_FEATURES if (key in self.flags.deep_cols)]
        fv_list = [self.build_dense_layer(features[key]) for key in self.NUMERICAL_FEATURES if (key in self.flags.deep_cols)]
        deep_list = self.concat((fv_list + ev_list))
    else:
        ev_list = [self.EmbeddingDict[key](features[key]) for key in self.CATEGORY_FEATURES]
        fv_list = [self.build_dense_layer(features[key]) for key in self.NUMERICAL_FEATURES]
        deep_list = self.concat((fv_list + ev_list))
    return (tf.concat(wide_list, (- 1)), tf.concat(deep_list, (- 1)))
