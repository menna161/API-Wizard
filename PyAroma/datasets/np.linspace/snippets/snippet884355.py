import argparse
import os
import xml.etree.ElementTree as ElementTree
from datetime import datetime
import numpy as np
import tensorflow as tf
from voc_to_hdf5 import get_ids


def process_dataset(name, image_paths, anno_paths, result_path, num_shards):
    "Process selected Pascal VOC dataset to generate TFRecords files.\n\n    Parameters\n    ----------\n    name : string\n        Name of resulting dataset 'train' or 'test'.\n    image_paths : list\n        List of paths to images to include in dataset.\n    anno_paths : list\n        List of paths to corresponding image annotations.\n    result_path : string\n        Path to put resulting TFRecord files.\n    num_shards : int\n        Number of shards to split TFRecord files into.\n    "
    shard_ranges = np.linspace(0, len(image_paths), (num_shards + 1)).astype(int)
    counter = 0
    for shard in range(num_shards):
        output_filename = '{}-{:05d}-of-{:05d}'.format(name, shard, num_shards)
        output_file = os.path.join(result_path, output_filename)
        writer = tf.python_io.TFRecordWriter(output_file)
        shard_counter = 0
        files_in_shard = range(shard_ranges[shard], shard_ranges[(shard + 1)])
        for i in files_in_shard:
            image_file = image_paths[i]
            anno_file = anno_paths[i]
            (image_data, height, width) = process_image(image_file)
            boxes = process_anno(anno_file)
            example = convert_to_example(image_data, boxes, image_file, height, width)
            writer.write(example.SerializeToString())
            shard_counter += 1
            counter += 1
            if (not (counter % 1000)):
                print('{} : Processed {:d} of {:d} images.'.format(datetime.now(), counter, len(image_paths)))
        writer.close()
        print('{} : Wrote {} images to {}'.format(datetime.now(), shard_counter, output_filename))
    print('{} : Wrote {} images to {} shards'.format(datetime.now(), counter, num_shards))
