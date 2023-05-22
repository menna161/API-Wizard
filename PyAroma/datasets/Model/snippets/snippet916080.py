import numpy as np
from sklearn.metrics import accuracy_score
import pytest
from transformers import BertForMultipleChoice, BertConfig
from mcqa.models import Model


def test_save_load(trained_model, mcqa_dataset, tmpdir):
    model_path = str(tmpdir)
    trained_model.save_model(model_path)
    mdl_clone = Model(bert_model='bert-base-uncased', device='cpu')
    config = BertConfig.from_pretrained(model_path, num_labels=4)
    mdl_clone.model = BertForMultipleChoice.from_pretrained(model_path, config=config)
    for (param1, param2) in zip(mdl_clone.model.parameters(), trained_model.model.parameters()):
        assert param1.data.allclose(param2.data)
    mdl_clone.fit(mcqa_dataset.get_dataset(), train_batch_size=1, num_train_epochs=1)
    _ = mdl_clone.predict_proba(mcqa_dataset.get_dataset(), eval_batch_size=1)
