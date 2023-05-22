import pytest
import numpy as np
from matchzoo.preprocessors import units
import matchzoo as mz
import tempfile
import os


def test_this():
    train_data = mz.datasets.toy.load_data()
    test_data = mz.datasets.toy.load_data(stage='test')
    dssm_preprocessor = mz.preprocessors.DSSMPreprocessor()
    train_data_processed = dssm_preprocessor.fit_transform(train_data, verbose=0)
    type(train_data_processed)
    test_data_transformed = dssm_preprocessor.transform(test_data)
    type(test_data_transformed)
