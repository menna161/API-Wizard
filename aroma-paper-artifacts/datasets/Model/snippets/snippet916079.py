import numpy as np
from sklearn.metrics import accuracy_score
import pytest
from transformers import BertForMultipleChoice, BertConfig
from mcqa.models import Model


def test_fit_reproducibility(trained_model, mcqa_dataset):
    mdl1 = trained_model
    mdl2 = Model(bert_model='bert-base-uncased', device='cpu')
    mdl2.fit(mcqa_dataset.get_dataset(), train_batch_size=1, num_train_epochs=1)
    for (param1, param2) in zip(mdl1.model.parameters(), mdl2.model.parameters()):
        assert param1.data.allclose(param2.data)
