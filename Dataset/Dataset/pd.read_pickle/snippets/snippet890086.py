from fire import Fire
from pathlib import Path
from axcell.data.paper_collection import PaperCollection
from axcell.data.structure import CellEvidenceExtractor
from elasticsearch_dsl import connections
from tqdm import tqdm
import pandas as pd
from joblib import delayed, Parallel


def merge_evidences(self, output='evidences.pkl', pattern='pc-parts/pc-part-*.evidences.pkl'):
    pickles = sorted(Path('.').glob(pattern))
    evidences = [pd.read_pickle(pickle) for pickle in pickles]
    evidences = pd.concat(evidences)
    evidences.to_pickle(output)
