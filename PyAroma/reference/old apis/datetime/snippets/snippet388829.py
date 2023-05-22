from util import *
import argparse
import xgboost as xgb
from catboost import CatBoostClassifier
import gc
from lightgbm import LGBMClassifier

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--frac', type=float, default=config.frac)
    parser.add_argument('--round', type=int, default=config.round)
    parser.add_argument('--train_data', type=str, default=f'{config.label_name}3')
    seed_everything(2019)
    args = parser.parse_args()
    frac = args.frac
    total_round = args.round
    train_data = args.train_data
    model_type = 'lgb'
    day = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    logger.info('day %s params %s', day, args)
    logger = configure_logging(('train_' + day))
    label = sample_label(load1(train_data, 0), frac)
    label1 = sample_label(load1(train_data, 1), frac)
    logger.info('label %s, label1 %s', len(label), len(label1))
    label = pd.concat((label, label1))
    del label1
    logger.info('final train data %s', label.shape)
    gc.collect()
    org_label_size = len(label)
    cat_cols = ['gender', 'freq', 'uf_c1', 'uf_c2', 'uf_c3', 'uf_c4', 'uf_c5', 'weekday', 'hour']
    for col in ['topic', 'follow_topic', 'inter_topic']:
        if (col in label):
            del label[col]
    gc.collect()
    feature_cols = [x for x in label.columns if (x not in drop_feature)]
    logger.info('feature size %s, %s', len(feature_cols), feature_cols)
    y_train_all = label['label']
    n_fold = 5
    fold = StratifiedKFold(n_splits=n_fold, shuffle=True, random_state=42)
    feature_df = pd.DataFrame()
    label = label[feature_cols]
    y_train = y_train_all
    for (index, (train_idx, val_idx)) in enumerate(fold.split(X=label, y=y_train_all)):
        if (index > 0):
            break
        (X_val, y_val) = (label.iloc[val_idx], y_train_all.iloc[val_idx])
        model = get_model()
        model.fit(label, y_train, eval_metric=['logloss', 'auc'], eval_set=[(X_val, y_val)], verbose=50, early_stopping_rounds=50)
        y_pred = model.predict_proba(X_val)[:, 1]
        filename = config.model_name
        dump_pkl(model, filename)
        auc = metrics.roc_auc_score(y_val, y_pred)
        logger.info('model %s, fold %s, auc %s ', filename, index, auc)
        fold_feature_df = pd.DataFrame()
        fold_feature_df['feature'] = feature_cols
        fold_feature_df['importance'] = model.feature_importances_
        fold_feature_df['fold'] = index
        feature_df = pd.concat([feature_df, fold_feature_df], axis=0)
        gc.collect()
    t = feature_df[['feature', 'importance']].groupby(['feature'])['importance'].mean().sort_values(ascending=False)
    logger.info('%s', t)
    logger.info('feature size %s', len(t))
    logger.info(t.head(100))
    t.to_csv(f'../feature/importance_{day}_{model_type}.csv')
