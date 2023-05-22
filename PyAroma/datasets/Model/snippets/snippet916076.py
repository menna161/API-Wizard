import numpy as np
from sklearn.metrics import accuracy_score
import pytest
from transformers import BertForMultipleChoice, BertConfig
from mcqa.models import Model


@pytest.fixture()
def trained_model(mcqa_dataset):
    mdl = Model(bert_model='bert-base-uncased', device='cpu')
    mdl.fit(mcqa_dataset.get_dataset(), train_batch_size=1, num_train_epochs=1)
    (yield mdl)
