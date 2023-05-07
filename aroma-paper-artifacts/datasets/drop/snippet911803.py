from torch.utils import data
from torch.utils.data.sampler import SequentialSampler, RandomSampler
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from .datasets.train_wheat import train_wheat
from .datasets.test_wheat import test_wheat
from .transforms import build_transforms
from .transforms import get_test_transform
from .collate_batch import collate_batch


def split_dataset(cfg):
    marking = pd.read_csv(f'{cfg.DATASETS.ROOT_DIR}/train.csv')
    bboxs = np.stack(marking['bbox'].apply((lambda x: np.fromstring(x[1:(- 1)], sep=','))))
    for (i, column) in enumerate(['x', 'y', 'w', 'h']):
        marking[column] = bboxs[(:, i)]
    marking.drop(columns=['bbox'], inplace=True)
    marking['area'] = (marking['w'] * marking['h'])
    marking = marking[(marking['area'] < 154200.0)]
    error_bbox = [100648.0, 145360.0, 149744.0, 119790.0, 106743.0]
    marking = marking[(~ marking['area'].isin(error_bbox))]
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    df_folds = marking[['image_id']].copy()
    df_folds.loc[(:, 'bbox_count')] = 1
    df_folds = df_folds.groupby('image_id').count()
    df_folds.loc[(:, 'source')] = marking[['image_id', 'source']].groupby('image_id').min()['source']
    df_folds.loc[(:, 'stratify_group')] = np.char.add(df_folds['source'].values.astype(str), df_folds['bbox_count'].apply((lambda x: f'_{(x // 15)}')).values.astype(str))
    df_folds.loc[(:, 'fold')] = 0
    for (fold_number, (train_index, val_index)) in enumerate(skf.split(X=df_folds.index, y=df_folds['stratify_group'])):
        df_folds.loc[(df_folds.iloc[val_index].index, 'fold')] = fold_number
    train_ids = df_folds[(df_folds['fold'] != cfg.DATASETS.VALID_FOLD)].index.values
    valid_ids = df_folds[(df_folds['fold'] == cfg.DATASETS.VALID_FOLD)].index.values
    if cfg.DEBUG:
        train_ids = train_ids[:40]
        valid_ids = valid_ids[:10]
    return (marking, train_ids, valid_ids)
