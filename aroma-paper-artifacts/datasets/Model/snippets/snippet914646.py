import keras.backend as K
import keras.layers as L
from keras.models import Model
import models.ima as ima


def build_model(char_size=27, training=True, goals=None, num_preds=2, pred_len=6):
    'Build the model.'
    context = L.Input(shape=(None, None, None), name='subcontext', dtype='int32')
    query = L.Input(shape=(None,), name='outer_query', dtype='int32')
    goals = (goals or list())
    templates = list()
    for (i, g) in enumerate(goals):
        t = RuleTemplate(g, num_preds, pred_len, char_size, name=('trule' + str(i)))(context)
        templates.append(t)
    if (len(templates) >= 2):
        templates = L.concatenate(templates, axis=1)
    else:
        templates = templates[0]
    (auxs, out) = ima.build_model(char_size, ilp=[context, query, templates])
    if training:
        model = Model([context, query], [out])
    else:
        model = Model([context, query], (([templates] + auxs) + [out]))
    for l in model.layers:
        if (not isinstance(l, RuleTemplate)):
            l.trainable = False
    if training:
        model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['acc'])
    return model
