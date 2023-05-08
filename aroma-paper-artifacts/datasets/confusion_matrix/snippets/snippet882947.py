import os
from fasttext import train_supervised
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix
import printcm
import yaml
import pprint
from tabulate import tabulate
import tools


def train(saveModel=True):
    train_data = tools.config()['model']['train-file']
    valid_data = tools.config()['model']['valid-file']
    quantizeModel = tools.config()['model']['quantize']
    extendedValidation = tools.config()['model']['print-confusion-matrix']
    traningParameters = tools.config()['model']['fasttext']
    traningParameters['input'] = train_data
    pp = pprint.PrettyPrinter(depth=1)
    print('\n traing with following parameters ')
    pp.pprint(traningParameters)
    model = train_supervised(**traningParameters)
    if quantizeModel:
        print('quantize model')
        model.quantize(input=train_data, thread=16, qnorm=True, retrain=True, cutoff=400000)
    if saveModel:
        path = tools.config()['model']['model-path']
        if quantizeModel:
            model.save_model((path + '.ftz'))
        else:
            model.save_model((path + '.bin'))
        with open((path + '.params'), 'w') as text_file:
            print(yaml.dump(tools.config()), file=text_file)
    if (extendedValidation is False):
        print_results(*model.test(valid_data))
    else:
        data = loadValidData(valid_data)
        truth = [row[0].replace('__label__', '') for row in data]
        texts = [row[1] for row in data]
        predictions = model.predict(texts)
        predictions = tools.flatmap(predictions[0])
        predicted = [x.replace('__label__', '') for x in predictions]
        (precision, recall, fscore, support) = score(truth, predicted)
        headers = ['metric', 'negative', 'neutral', 'positive']
        table = []
        table.append((['precision'] + [x for x in precision]))
        table.append((['recall'] + [x for x in recall]))
        table.append((['fscore'] + [x for x in fscore]))
        table.append((['sample count'] + [x for x in support]))
        print(tabulate(table, headers, tablefmt='pipe', floatfmt='.4f'))
        (precision, recall, fscore, support) = score(truth, predicted, average='macro')
        print('macro fscore: {}'.format(fscore))
        (precision, recall, fscore, support) = score(truth, predicted, average='micro')
        print('micro fscore: {}'.format(fscore))
        cm = confusion_matrix(truth, predicted, labels=['negative', 'neutral', 'positive'])
        printcm.plot_confusion_matrix(cm=cm, target_names=['negative', 'neutral', 'positive'], normalize=True, title='sentiment classification')
    return model
