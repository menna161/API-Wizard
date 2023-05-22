import numpy as np
from sklearn.metrics import accuracy_score
import pytest
from transformers import BertForMultipleChoice, BertConfig
from mcqa.models import Model


def test_unfitted_error(mcqa_dataset):
    mdl = Model(bert_model='bert-base-uncased', device='cpu')
    with pytest.raises(Exception):
        mdl.predict_proba(mcqa_dataset.get_dataset(), eval_batch_size=1)
