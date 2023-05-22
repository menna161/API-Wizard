import tensorflow as tf
import time
from configuration import IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS, EPOCHS, NUM_CLASSES, BATCH_SIZE, save_model_dir, load_weights_from_epoch, save_frequency, test_images_during_training, test_images_dir_list
from core.ground_truth import ReadDataset
from core.loss import MultiBoxLoss
from core.make_dataset import TFDataset
from core.ssd import SSD
from utils.visualize import visualize_training_results


def print_model_summary(network):
    sample_inputs = tf.random.normal(shape=(1, IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS))
    _ = network(sample_inputs, training=True)
    network.summary()
