import random
from typing import Dict, List, Union
import lightgbm as lgb
import pandas as pd
from spaceopt.space import Space


def _sample_unevaluated_unique_spoints(self, sample_size: int, max_num_retries: int=100) -> List[dict]:
    self._verify_sample_size(sample_size)
    self._verify_max_num_retries(max_num_retries)
    if (len(self.evaluated_spoints) > 0):
        evaluated_spoints_df = pd.DataFrame(self.evaluated_spoints)
        evaluated_spoints_df = evaluated_spoints_df[self.space.variable_names]
        evaluated_spoints_df = evaluated_spoints_df.drop_duplicates()
        num_unique_evaluated_spoints = len(evaluated_spoints_df)
    else:
        num_unique_evaluated_spoints = 0
    max_sample_size = min(sample_size, (self.space.size - num_unique_evaluated_spoints))
    sampled_spoints = []
    for i in range(max_num_retries):
        sampled_spoints += self._sample_random_spoints(sample_size=sample_size)
        sampled_spoints_df = pd.DataFrame(sampled_spoints)
        sampled_spoints_df = sampled_spoints_df.drop_duplicates()
        if (num_unique_evaluated_spoints > 0):
            sampled_spoints_df = sampled_spoints_df.merge(right=evaluated_spoints_df, on=self.space.variable_names, how='left', indicator=True)
            indicator_left_only = sampled_spoints_df['_merge'].eq('left_only')
            sampled_spoints_df = sampled_spoints_df[indicator_left_only]
            sampled_spoints_df = sampled_spoints_df.drop(columns='_merge')
        sampled_spoints = sampled_spoints_df.to_dict('records')
        if (len(sampled_spoints) >= max_sample_size):
            break
    sampled_spoints = sampled_spoints[:max_sample_size]
    if (len(sampled_spoints) == 0):
        raise RuntimeError(f'''could not sample any new spoints - search_space is fully explored or random sampling was unfortunate.
search_space.size = {self.space.size}
num evaluated spoints = {len(self.evaluated_spoints)}
num unevaluated spoints = {(self.space.size - len(self.evaluated_spoints))}''')
    random.shuffle(sampled_spoints)
    return sampled_spoints
