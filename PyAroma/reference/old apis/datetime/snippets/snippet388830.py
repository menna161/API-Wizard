from util import *
import argparse
import xgboost as xgb
from lightgbm import LGBMClassifier
import gc

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--frac', type=float, default=0.2)
    parser.add_argument('--model_name', type=str, default=config.model_name)
    parser.add_argument('--train_data', type=str, default=f'{config.label_name}3')
    parser.add_argument('--result', type=str, default='result')
    seed_everything(2019)
    args = parser.parse_args()
    frac = args.frac
    model_name = args.model_name
    train_data = args.train_data
    result_name = args.result
    day = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    logger.info('day %s params %s', day, args)
    logger = configure_logging(('train_' + day))
    label = sample_label(load_h5(f'{train_data}_0.h5'), frac)
    label1 = sample_label(load_h5(f'{train_data}_1.h5'), frac)
    label = pd.concat((label, label1))
    del label1
    test = load_h5(f'{train_data}_2.h5')
    sub = test[['index']].copy()
    gc.collect()
    org_label_size = len(label)
    cat_cols = ['gender', 'freq', 'uf_c1', 'uf_c2', 'uf_c3', 'uf_c4', 'uf_c5', 'weekday', 'hour']
    for col in ['topic', 'follow_topic', 'inter_topic']:
        if (col in label):
            del label[col]
    gc.collect()
    feature_cols = [x for x in label.columns if (x not in drop_feature)]
    logger.info('feature size %s, %s', len(feature_cols), feature_cols)
    test = test[feature_cols]
    y_train_all = label['label']
    n_fold = 5
    fold = StratifiedKFold(n_splits=n_fold, shuffle=True, random_state=42)
    feature_df = pd.DataFrame()
    subPreds = np.zeros(test.shape[0])
    for (index, (train_idx, val_idx)) in enumerate(fold.split(X=label, y=y_train_all)):
        if (index > 0):
            break
        (X_val, y_val) = (label.iloc[val_idx][feature_cols], y_train_all.iloc[val_idx])
    del label
    gc.collect()
    split = model_name.split(',')
    for name in split:
        model = load_pkl(name)
        y_pred = model.predict_proba(X_val)[:, 1]
        auc = metrics.roc_auc_score(y_val, y_pred)
        logger.info('model %s auc %s', name, auc)
        subPreds += (model.predict_proba(test)[:, 1] / len(split))
        del model
        gc.collect()
    sub['label'] = subPreds
    dump_h5(sub, f'{result_name}_sub.h5')
    check_result(3, sub, result_name)
