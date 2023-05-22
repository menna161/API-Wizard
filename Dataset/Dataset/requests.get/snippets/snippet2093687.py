import logging
import networkx as nx
import numpy as np
from scipy import optimize, spatial
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors


def query_topn(model, top_n=10, head=None, relation=None, tail=None, ents_to_consider=None, rels_to_consider=None):
    "Queries the model with two elements of a triple and returns the top_n results of\n    all possible completions ordered by score predicted by the model.\n\n    For example, given a `<subject, predicate>` pair in the arguments, the model will score\n    all possible triples `<subject, predicate, ?>`, filling in the missing element with known\n    entities, and return the top_n triples ordered by score. If given a `<subject, object>`\n    pair it will fill in the missing element with known relations.\n\n    .. note::\n        This function does not filter out true statements - triples returned can include those\n        the model was trained on.\n\n    Parameters\n    ----------\n    model : EmbeddingModel\n        The trained model that will be used to score triple completions.\n    top_n : int\n        The number of completed triples to returned.\n    head : str\n        An entity string to query.\n    relation : str\n        A relation string to query.\n    tail : str\n        An object string to query.\n    ents_to_consider: array-like\n        List of entities to use for triple completions. If `None`, will generate completions using all distinct entities\n        (Default: `None`).\n    rels_to_consider: array-like\n        List of relations to use for triple completions. If `None`, will generate completions using all distinct\n        relations (default: `None`).\n\n    Returns\n    -------\n    X : ndarray of shape (n, 3)\n        A list of triples ordered by score.\n    S : ndarray, shape (n)\n       A list of scores.\n\n    Example\n    -------\n\n    >>> import requests\n    >>> from ampligraph.datasets import load_from_csv\n    >>> from ampligraph.discovery import discover_facts\n    >>> from ampligraph.discovery import query_topn\n    >>> from ampligraph.latent_features import ScoringBasedEmbeddingModel\n    >>> # Game of Thrones relations dataset\n    >>> url = 'https://ampligraph.s3-eu-west-1.amazonaws.com/datasets/GoT.csv'\n    >>> open('GoT.csv', 'wb').write(requests.get(url).content)\n    >>> X = load_from_csv('.', 'GoT.csv', sep=',')\n    >>>\n    >>> model = ScoringBasedEmbeddingModel(eta=5,\n    >>>                                    k=150,\n    >>>                                    scoring_type='TransE')\n    >>> model.compile(optimizer='adagrad', loss='pairwise')\n    >>> model.fit(X,\n    >>>           batch_size=100,\n    >>>           epochs=20,\n    >>>           verbose=False)\n    >>>\n    >>> query_topn(model, top_n=5,\n    >>>            head='Eddard Stark', relation='ALLIED_WITH', tail=None,\n    >>>            ents_to_consider=None, rels_to_consider=None)\n    >>>\n    (array([['Eddard Stark', 'ALLIED_WITH', 'Smithyton'],\n            ['Eddard Stark', 'ALLIED_WITH', 'Eden Risley'],\n            ['Eddard Stark', 'ALLIED_WITH', 'House Westbrook'],\n            ['Eddard Stark', 'ALLIED_WITH', 'House Leygood'],\n            ['Eddard Stark', 'ALLIED_WITH', 'House Bridges']], dtype='<U44'),\n     array([9.000417 , 5.272001 , 5.1876183, 5.121145 , 5.0564814],\n           dtype=float32))\n\n    "
    if model.is_backward:
        model = model.model
    if (not model.is_fitted):
        msg = 'Model is not fitted.'
        logger.error(msg)
        raise ValueError(msg)
    if (not (np.sum([(head is None), (relation is None), (tail is None)]) == 1)):
        msg = 'Exactly one of `head`, `relation` or `tail` arguments must be None.'
        logger.error(msg)
        raise ValueError(msg)
    if head:
        if (head not in list(model.data_indexer.backend.get_all_entities())):
            msg = 'Head entity `{}` not seen by model'.format(head)
            logger.error(msg)
            raise ValueError(msg)
    if relation:
        if (relation not in list(model.data_indexer.backend.get_all_relations())):
            msg = 'Relation `{}` not seen by model'.format(relation)
            logger.error(msg)
            raise ValueError(msg)
    if tail:
        if (tail not in list(model.data_indexer.backend.get_all_entities())):
            msg = 'Tail entity `{}` not seen by model'.format(tail)
            logger.error(msg)
            raise ValueError(msg)
    if (ents_to_consider is not None):
        if (head and tail):
            msg = 'Cannot specify `ents_to_consider` and both `subject` and `object` arguments.'
            logger.error(msg)
            raise ValueError(msg)
        if (not isinstance(ents_to_consider, (list, np.ndarray))):
            msg = '`ents_to_consider` must be a list or numpy array.'
            logger.error(msg)
            raise ValueError(msg)
        if (not all(((x in list(model.data_indexer.backend.get_all_entities())) for x in ents_to_consider))):
            msg = 'Entities in `ents_to_consider` have not been seen by the model.'
            logger.error(msg)
            raise ValueError(msg)
        if (len(ents_to_consider) < top_n):
            msg = '`ents_to_consider` contains less than top_n values, return set will be truncated.'
            logger.warning(msg)
    if (rels_to_consider is not None):
        if relation:
            msg = 'Cannot specify both `rels_to_consider` and `relation` arguments.'
            logger.error(msg)
            raise ValueError(msg)
        if (not isinstance(rels_to_consider, (list, np.ndarray))):
            msg = '`rels_to_consider` must be a list or numpy array.'
            logger.error(msg)
            raise ValueError(msg)
        if (not all(((x in list(model.data_indexer.backend.get_all_relations())) for x in rels_to_consider))):
            msg = 'Relations in `rels_to_consider` have not been seen by the model.'
            logger.error(msg)
            raise ValueError(msg)
        if (len(rels_to_consider) < top_n):
            msg = '`rels_to_consider` contains less than top_n values, return set will be truncated.'
            logger.warning(msg)
    if (relation is None):
        rels = (rels_to_consider or list(model.data_indexer.backend.get_all_relations()))
        triples = np.array([[head, x, tail] for x in rels])
    else:
        ents = (ents_to_consider or list(model.data_indexer.backend.get_all_entities()))
        if head:
            triples = np.array([[head, relation, x] for x in ents])
        else:
            triples = np.array([[x, relation, tail] for x in ents])
    scores = model.predict(triples)
    topn_idx = np.squeeze(np.argsort(scores, axis=0)[::(- 1)][:top_n])
    scores_out = np.array(scores)[topn_idx]
    triples_out = np.copy(triples[(topn_idx, :)])
    return (triples_out, scores_out)
