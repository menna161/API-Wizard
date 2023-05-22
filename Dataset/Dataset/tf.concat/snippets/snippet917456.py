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


def create_model(inputs, targets, reuse_bool=False):
    batchSize = tf.shape(inputs)[0]
    surfaceArray = []
    if ((a.loss == 'render') or (a.loss == 'renderL2')):
        XsurfaceArray = tf.expand_dims(tf.lin_space((- 1.0), 1.0, CROP_SIZE), axis=(- 1))
        XsurfaceArray = tf.tile(XsurfaceArray, [1, CROP_SIZE])
        YsurfaceArray = ((- 1) * tf.transpose(XsurfaceArray))
        XsurfaceArray = tf.expand_dims(XsurfaceArray, axis=(- 1))
        YsurfaceArray = tf.expand_dims(YsurfaceArray, axis=(- 1))
        surfaceArray = tf.concat([XsurfaceArray, YsurfaceArray, tf.zeros([CROP_SIZE, CROP_SIZE, 1], dtype=tf.float32)], axis=(- 1))
        surfaceArray = tf.expand_dims(surfaceArray, axis=0)
    with tf.variable_scope('generator', reuse=reuse_bool) as scope:
        out_channels = 9
        outputs = create_generator(inputs, out_channels)
    partialOutputedNormals = outputs[(:, :, :, 0:2)]
    outputedDiffuse = outputs[(:, :, :, 2:5)]
    outputedRoughness = outputs[(:, :, :, 5)]
    outputedSpecular = outputs[(:, :, :, 6:9)]
    normalShape = tf.shape(partialOutputedNormals)
    newShape = [normalShape[0], normalShape[1], normalShape[2], 1]
    tmpNormals = tf.ones(newShape, tf.float32)
    normNormals = tf_Normalize(tf.concat([partialOutputedNormals, tmpNormals], axis=(- 1)))
    outputedRoughnessExpanded = tf.expand_dims(outputedRoughness, axis=(- 1))
    reconstructedOutputs = tf.concat([normNormals, outputedDiffuse, outputedRoughnessExpanded, outputedRoughnessExpanded, outputedRoughnessExpanded, outputedSpecular], axis=(- 1))
    with tf.name_scope('generator_loss'):
        gen_loss_L1 = 0
        rerenderedTargets = []
        rerenderedOutputs = []
        renderedDiffuseImages = []
        renderedDiffuseImagesOutputs = []
        renderedSpecularImages = []
        renderedSpecularImagesOutputs = []
        outputs = reconstructedOutputs
        if (a.loss == 'l1'):
            epsilon = 0.001
            NormalL1 = (tf.abs((targets[(0, :, :, 0:3)] - outputs[(0, :, :, 0:3)])) * a.normalLossFactor)
            DiffuseL1 = (tf.abs((tf.log((epsilon + deprocess(targets[(0, :, :, 3:6)]))) - tf.log((epsilon + deprocess(outputs[(0, :, :, 3:6)]))))) * a.diffuseLossFactor)
            RoughnessL1 = (tf.abs((targets[(0, :, :, 6:9)] - outputs[(0, :, :, 6:9)])) * a.roughnessLossFactor)
            SpecularL1 = (tf.abs((tf.log((epsilon + deprocess(targets[(0, :, :, 9:12)]))) - tf.log((epsilon + deprocess(outputs[(0, :, :, 9:12)]))))) * a.specularLossFactor)
            gen_loss_L1 = tf.reduce_mean((((NormalL1 + DiffuseL1) + SpecularL1) + RoughnessL1))
        elif (a.loss == 'l2'):
            epsilon = 0.001
            NormalL1 = (tf.square((targets[(0, :, :, 0:3)] - outputs[(0, :, :, 0:3)])) * a.normalLossFactor)
            DiffuseL1 = (tf.square((tf.log((epsilon + deprocess(targets[(0, :, :, 3:6)]))) - tf.log((epsilon + deprocess(outputs[(0, :, :, 3:6)]))))) * a.diffuseLossFactor)
            RoughnessL1 = (tf.square((targets[(0, :, :, 6:9)] - outputs[(0, :, :, 6:9)])) * a.roughnessLossFactor)
            SpecularL1 = (tf.square((tf.log((epsilon + deprocess(targets[(0, :, :, 9:12)]))) - tf.log((epsilon + deprocess(outputs[(0, :, :, 9:12)]))))) * a.specularLossFactor)
            gen_loss_L1 = tf.reduce_mean((((NormalL1 + DiffuseL1) + SpecularL1) + RoughnessL1))
        elif ((a.loss == 'render') or (a.loss == 'renderL2')):
            with tf.name_scope('renderer'):
                with tf.name_scope('diffuse'):
                    for nbDiffuseRender in range(a.nbDiffuseRendering):
                        diffuses = tf_generateDiffuseRendering(batchSize, targets, outputs)
                        renderedDiffuseImages.append(diffuses[0][0])
                        renderedDiffuseImagesOutputs.append(diffuses[1][0])
                with tf.name_scope('specular'):
                    for nbspecularRender in range(a.nbSpecularRendering):
                        speculars = tf_generateSpecularRendering(batchSize, surfaceArray, targets, outputs)
                        renderedSpecularImages.append(speculars[0][0])
                        renderedSpecularImagesOutputs.append(speculars[1][0])
                rerenderedTargets = renderedDiffuseImages[0]
                for renderingDiff in renderedDiffuseImages[1:]:
                    rerenderedTargets = tf.concat([rerenderedTargets, renderingDiff], axis=(- 1))
                for renderingSpecu in renderedSpecularImages:
                    rerenderedTargets = tf.concat([rerenderedTargets, renderingSpecu], axis=(- 1))
                rerenderedOutputs = renderedDiffuseImagesOutputs[0]
                for renderingOutDiff in renderedDiffuseImagesOutputs[1:]:
                    rerenderedOutputs = tf.concat([rerenderedOutputs, renderingOutDiff], axis=(- 1))
                for renderingOutSpecu in renderedSpecularImagesOutputs:
                    rerenderedOutputs = tf.concat([rerenderedOutputs, renderingOutSpecu], axis=(- 1))
                gen_loss_L1 = 0
                if (a.loss == 'render'):
                    gen_loss_L1 = tf.reduce_mean(tf.abs((tf.log((rerenderedTargets + 0.01)) - tf.log((rerenderedOutputs + 0.01)))))
                if (a.loss == 'renderL2'):
                    gen_loss_L1 = tf.reduce_mean(tf.square((tf.log((rerenderedTargets + 0.01)) - tf.log((rerenderedOutputs + 0.01)))))
        consistencyLoss = 0
        gen_loss = (gen_loss_L1 * a.l1_weight)
    with tf.name_scope('generator_train'):
        with tf.variable_scope('generator_train0', reuse=reuse_bool):
            gen_tvars = [var for var in tf.trainable_variables() if var.name.startswith('generator')]
            gen_optim = tf.train.AdamOptimizer(a.lr, a.beta1)
            gen_grads_and_vars = gen_optim.compute_gradients(gen_loss_L1, var_list=gen_tvars)
            gen_train = gen_optim.apply_gradients(gen_grads_and_vars)
    ema = tf.train.ExponentialMovingAverage(decay=0.99)
    update_losses = ema.apply([gen_loss_L1])
    global_step = tf.train.get_or_create_global_step()
    incr_global_step = tf.assign(global_step, (global_step + 1))
    return Model(gen_loss_L1_exact=gen_loss_L1, gen_loss_L1=ema.average(gen_loss_L1), gen_grads_and_vars=gen_grads_and_vars, outputs=outputs, train=tf.group(update_losses, incr_global_step, gen_train), rerendered=[rerenderedTargets, rerenderedOutputs])
