import logging
import os
import pytest
import numpy as np
import librosa
from sonosco.common.constants import SONOSCO
from sonosco.common.utils import setup_logging
from sonosco.datasets.dataset import AudioDataset, AudioDataProcessor
from sonosco.datasets.samplers import BucketingSampler
from sonosco.datasets.loader import DataLoader
from sonosco.datasets.download_datasets.librispeech import try_download_librispeech


def test_librispeech_clean(logger):
    audio_conf = dict(sample_rate=SAMPLE_RATE, window_size=0.02, window_stride=0.01, labels='ABCDEFGHIJKLMNOPQRSTUVWXYZ', normalize=True, augment=False)
    processor = AudioDataProcessor(**audio_conf)
    manifest_directory = os.path.join(os.path.expanduser('~'), LIBRI_SPEECH_DIR)
    test_manifest = os.path.join(manifest_directory, 'libri_test_clean_manifest.csv')
    if (not os.path.exists(test_manifest)):
        try_download_librispeech(LIBRI_SPEECH_DIR, SAMPLE_RATE, ['test-clean.tar.gz', 'test-other.tar.gz'], 1, 15)
    assert os.path.exists(test_manifest)
    test_dataset = AudioDataset(processor, manifest_filepath=test_manifest)
    logger.info('Dataset is created')
    if os.path.exists(TEST_WAVS_DIR):
        os.removedirs(TEST_WAVS_DIR)
    os.makedirs(TEST_WAVS_DIR)
    n_samples = len(test_dataset)
    ids = np.random.randint(n_samples, size=min(10, n_samples))
    for index in ids:
        (sound, transcription) = test_dataset.get_raw(index)
        librosa.output.write_wav(os.path.join(TEST_WAVS_DIR, f'audio_{index}.wav'), sound, SAMPLE_RATE)
