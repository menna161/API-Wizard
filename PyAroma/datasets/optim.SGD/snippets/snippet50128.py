import random
import numpy as np
import torch
from transformers import RobertaForSequenceClassification, RobertaTokenizer, PretrainedConfig
import sys
from evidence_inference.preprocess.preprocessor import get_Xy, train_document_ids, test_document_ids, validation_document_ids, get_train_Xy
from transformers import AdamW


def train(train_Xy, n_epochs=4, batch_size=4):
    tokenizer = RobertaTokenizer.from_pretrained('allenai/biomed_roberta_base')
    model = RobertaForSequenceClassification.from_pretrained('allenai/biomed_roberta_base').to(device=device)
    from transformers import AdamW
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    best_val = np.inf
    train_epoch_loss = 0
    for epoch in range(n_epochs):
        model.train()
        print('on epoch ', epoch)
        train_epoch_loss = 0
        (batch_X, batch_y) = ([], [])
        cur_batch_size = 0
        for (i, article) in enumerate(train_Xy):
            if ((i % 100) == 0):
                print('on article', i)
            (cur_X, cur_y) = instances_from_article(article, max_instances=(batch_size - cur_batch_size))
            batch_X.extend(cur_X)
            batch_y.extend(cur_y)
            cur_batch_size += len(cur_X)
            if (cur_batch_size >= batch_size):
                optimizer.zero_grad()
                batch_X_tensor = tokenizer.batch_encode_plus(batch_X[:batch_size], max_length=512, add_special_tokens=True, pad_to_max_length=True)
                batch_y_tensor = torch.tensor(batch_y[:batch_size])
                (loss, logits) = model(torch.tensor(batch_X_tensor['input_ids']).to(device=device), attention_mask=torch.tensor(batch_X_tensor['attention_mask']).to(device=device), labels=batch_y_tensor.to(device=device))
                train_epoch_loss += loss.cpu().detach().numpy()
                loss.backward()
                optimizer.step()
                cur_batch_size = 0
                (batch_X, batch_y) = ([], [])
        print('total epoch train loss {}'.format(train_epoch_loss))
        print('evaluating on val...')
        model.eval()
        (total_correct, total_preds) = (0, 0)
        val_loss = 0
        for (j, article) in enumerate(val_Xy):
            (val_X, val_y) = instances_from_article(article, max_instances=batch_size)
            val_X_tensor = tokenizer.batch_encode_plus(val_X[:batch_size], max_length=512, add_special_tokens=True, pad_to_max_length=True)
            val_y_tensor = torch.tensor(val_y[:batch_size])
            (loss, logits) = model(torch.tensor(val_X_tensor['input_ids']).to(device=device), attention_mask=torch.tensor(val_X_tensor['attention_mask']).to(device=device), labels=torch.tensor(val_y_tensor).to(device=device))
            val_loss += loss.cpu().detach().numpy()
            class_preds = torch.argmax(logits, dim=1).detach().cpu()
            total_correct += (class_preds == val_y_tensor).sum()
            total_preds += len(val_X)
        val_acc = (total_correct / float(total_preds))
        print('val loss, acc after epoch {} is: {}, {}'.format(epoch, val_loss, val_acc))
        if (val_loss < best_val):
            print('new best loss: {}'.format(val_loss))
            best_val = val_loss
            torch.save(model.state_dict(), 'inference.model')
