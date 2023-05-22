import logging
import networkx as nx
import numpy as np
from scipy import optimize, spatial
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors


def find_duplicates(X, model, mode='e', metric='l2', tolerance='auto', expected_fraction_duplicates=0.1, verbose=False):
    '\n    Find duplicate entities, relations or triples in a graph based on their embeddings.\n\n    For example, say you have a movie dataset that was scraped off the web with possible duplicate movies.\n    The movies in this case are the entities.\n    Therefore, you would use the `"e"` mode to find all the movies that could de duplicates of each other.\n\n    Duplicates are defined as points whose distance in the embedding space are smaller than\n    some given threshold (called the tolerance).\n\n    The tolerance can be defined a priori or be found via an optimisation procedure given\n    an expected fraction of duplicates. The optimisation algorithm applies a root-finding routine\n    to find the tolerance that gets to the closest expected fraction. The routine always converges.\n\n    Distance is defined by the chosen metric, which by default is the Euclidean distance (L2 norm).\n\n    As the distances are calculated on the embedding space,\n    the embeddings must be meaningful for this routine to work properly.\n    Therefore, it is suggested to evaluate the embeddings first using a metric such as MRR\n    before considering applying this method.\n\n    Parameters\n    ----------\n\n    X : ndarray, shape (n, 3) or (n)\n        The input to be clustered.\n        `X` can either be the triples of a knowledge graph, its entities, or its relations.\n        The argument ``mode`` defines whether X is supposed to be an array of triples\n        or an array of either entities or relations.\n    model : EmbeddingModel\n        The fitted model that will be used to generate the embeddings.\n        This model must have been fully trained already, be it directly with ``fit()``\n        or from a helper function such as :meth:`ampligraph.evaluation.select_best_model_ranking`.\n    mode: str\n        Specifies among which type of entities to look for duplicates.\n\n        Choose from:\n\n        - | `\'e\'` (default): the algorithm will find duplicates of the provided entities based on their embeddings.\n        - | `\'r\'`: the algorithm will find duplicates of the provided relations based on their embeddings.\n        - | `\'t\'` : the algorithm will find duplicates of the concatenation\n            of the embeddings of the subject, predicate and object for each provided triple.\n\n    metric: str\n        A distance metric used to compare entity distance in the embedding space.\n        `See options here <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html>`_.\n    tolerance: int or str\n        Minimum distance (depending on the chosen ``metric``) to define one entity as the duplicate of another.\n        If `\'auto\'`, it will be determined automatically in a way that you get the ``expected_fraction_duplicates``.\n        The `\'auto\'` option can be much slower than the regular one, as the finding duplicate internal procedure\n        will be repeated multiple times.\n    expected_fraction_duplicates: float\n        Expected fraction of duplicates to be found. It is used only when ``tolerance=\'auto\'``.\n        Should be between 0 and 1 (default: 0.1).\n    verbose: bool\n        Whether to print evaluation messages during optimisation when ``tolerance=\'auto\'`` (default: `False`).\n\n    Returns\n    -------\n    duplicates : set of frozensets\n        Each entry in the duplicates set is a frozenset containing all entities that were found to be duplicates\n        according to the metric and tolerance.\n        Each frozenset will contain at least two entities.\n\n    tolerance: float\n        Tolerance used to find the duplicates (useful if the automatic tolerance option is selected).\n\n    Example\n    -------\n    >>> import pandas as pd\n    >>> import numpy as np\n    >>> import re\n    >>> from ampligraph.latent_features.models import ScoringBasedEmbeddingModel\n    >>> # The IMDB dataset used here is part of the Movies5 dataset found on:\n    >>> # The Magellan Data Repository (https://sites.google.com/site/anhaidgroup/projects/data)\n    >>> import requests\n    >>> url = \'http://pages.cs.wisc.edu/~anhai/data/784_data/movies5.tar.gz\'\n    >>> open(\'movies5.tar.gz\', \'wb\').write(requests.get(url).content)\n    >>> import tarfile\n    >>> tar = tarfile.open(\'movies5.tar.gz\', "r:gz")\n    >>> tar.extractall()\n    >>> tar.close()\n    >>>\n    >>> # Reading tabular dataset of IMDB movies and filling the missing values\n    >>> imdb = pd.read_csv("movies5/csv_files/imdb.csv")\n    >>> imdb["directors"] = imdb["directors"].fillna("UnknownDirector")\n    >>> imdb["actors"] = imdb["actors"].fillna("UnknownActor")\n    >>> imdb["genre"] = imdb["genre"].fillna("UnknownGenre")\n    >>> imdb["duration"] = imdb["duration"].fillna("0")\n    >>>\n    >>> # Creating knowledge graph triples from tabular dataset\n    >>> imdb_triples = []\n    >>>\n    >>> for _, row in imdb.iterrows():\n    >>>     movie_id = "ID" + str(row["id"])\n    >>>     directors = row["directors"].split(",")\n    >>>     actors = row["actors"].split(",")\n    >>>     genres = row["genre"].split(",")\n    >>>     duration = "Duration" + str(int(re.sub("\\D", "", row["duration"])) // 30)\n    >>>\n    >>>     directors_triples = [(movie_id, "hasDirector", d) for d in directors]\n    >>>     actors_triples = [(movie_id, "hasActor", a) for a in actors]\n    >>>     genres_triples = [(movie_id, "hasGenre", g) for g in genres]\n    >>>     duration_triple = (movie_id, "hasDuration", duration)\n    >>>\n    >>>\n    >>>     imdb_triples.extend(directors_triples)\n    >>>     imdb_triples.extend(actors_triples)\n    >>>     imdb_triples.extend(genres_triples)\n    >>>     imdb_triples.append(duration_triple)\n    >>>\n    >>> # Training knowledge graph embedding with ComplEx model\n    >>> from ampligraph.latent_features import ScoringBasedEmbeddingModel\n    >>>\n    >>> imdb_triples = np.array(imdb_triples)\n    >>> model = ScoringBasedEmbeddingModel(eta=5,\n    >>>                                    k=300,\n    >>>                                    scoring_type=\'ComplEx\')\n    >>> model.compile(optimizer=\'adam\', loss=\'multiclass_nll\')\n    >>> model.fit(imdb_triples,\n    >>>           batch_size=10000,\n    >>>           epochs=10)\n    >>>\n    >>> # Finding duplicates movies (entities)\n    >>> from ampligraph.discovery import find_duplicates\n    >>>\n    >>> entities = np.unique(imdb_triples[:, 0])\n    >>> dups, _ = find_duplicates(entities, model, mode=\'e\', tolerance=0.45)\n    >>> id_list = []\n    >>> for data in dups:\n    >>>     for i in data:\n    >>>         id_list.append(int(i[2:]))\n    >>> print(imdb.iloc[id_list[:6]][[\'movie_name\', \'year\']])\n    Epoch 1/10\n    7/7 [==============================] - 1s 122ms/step - loss: 15612.8799\n    Epoch 2/10\n    7/7 [==============================] - 0s 20ms/step - loss: 15610.5010\n    Epoch 3/10\n    7/7 [==============================] - 0s 19ms/step - loss: 15607.7412\n    Epoch 4/10\n    7/7 [==============================] - 0s 19ms/step - loss: 15604.0674\n    Epoch 5/10\n    7/7 [==============================] - 0s 20ms/step - loss: 15598.9365\n    Epoch 6/10\n    7/7 [==============================] - 0s 19ms/step - loss: 15591.7188\n    Epoch 7/10\n    7/7 [==============================] - 0s 19ms/step - loss: 15581.6055\n    Epoch 8/10\n    7/7 [==============================] - 0s 20ms/step - loss: 15567.6807\n    Epoch 9/10\n    7/7 [==============================] - 0s 20ms/step - loss: 15548.8184\n    Epoch 10/10\n    7/7 [==============================] - 0s 21ms/step - loss: 15523.8721\n               movie_name  year\n    5198    Duel to Death  1983\n    5199    Duel to Death  1983\n    2649   The Eliminator  2004\n    2650   The Eliminator  2004\n    3967  Lipstick Camera  1994\n    3968  Lipstick Camera  1994\n    '
    if model.is_backward:
        model = model.model
    if (not model.is_fitted):
        msg = 'Model has not been fitted.'
        logger.error(msg)
        raise ValueError(msg)
    modes = ('t', 'e', 'r')
    if (mode not in modes):
        msg = 'Argument `mode` must be one of the following: {}.'.format(', '.join(modes))
        logger.error(msg)
        raise ValueError(msg)
    if ((mode == 't') and ((len(X.shape) != 2) or (X.shape[1] != 3))):
        msg = "For 't' mode the input X must be a matrix with three columns."
        logger.error(msg)
        raise ValueError(msg)
    if ((mode in ('e', 'r')) and (len(X.shape) != 1)):
        msg = "For 'e' or 'r' mode the input X must be an array."
        logger.error(msg)
        raise ValueError(msg)
    if (mode == 't'):
        s = model.get_embeddings(X[(:, 0)], embedding_type='e')
        p = model.get_embeddings(X[(:, 1)], embedding_type='r')
        o = model.get_embeddings(X[(:, 2)], embedding_type='e')
        emb = np.hstack((s, p, o))
    else:
        emb = model.get_embeddings(X, embedding_type=mode)

    def get_dups(tol):
        '\n        Given tolerance, finds duplicate entities in a graph based on their embeddings.\n\n        Parameters\n        ----------\n        tol: float\n            Minimum distance (depending on the chosen metric) to define one entity as the duplicate of another.\n\n        Returns\n        -------\n        duplicates : set of frozensets\n            Each entry in the duplicates set is a frozenset containing all entities that were found to be duplicates\n            according to the metric and tolerance.\n            Each frozenset will contain at least two entities.\n\n        '
        nn = NearestNeighbors(metric=metric, radius=tol)
        nn.fit(emb)
        neighbors = nn.radius_neighbors(emb)[1]
        idx_dups = ((i, row) for (i, row) in enumerate(neighbors) if (len(row) > 1))
        if (mode == 't'):
            dups = {frozenset((tuple(X[idx]) for idx in row)) for (i, row) in idx_dups}
        else:
            dups = {frozenset((X[idx] for idx in row)) for (i, row) in idx_dups}
        return dups

    def opt(tol, info):
        '\n        Auxiliary function for the optimization procedure to find the tolerance that corresponds to the expected\n        number of duplicates.\n\n        Returns the difference between actual and expected fraction of duplicates.\n        '
        duplicates = get_dups(tol)
        fraction_duplicates = (len(set().union(*duplicates)) / len(emb))
        if verbose:
            info['Nfeval'] += 1
            logger.info('Eval {}: tol: {}, duplicate fraction: {}'.format(info['Nfeval'], tol, fraction_duplicates))
        return (fraction_duplicates - expected_fraction_duplicates)
    if (tolerance == 'auto'):
        max_distance = spatial.distance_matrix(emb, emb).max()
        tolerance = optimize.bisect(opt, 0.0, max_distance, xtol=0.001, maxiter=50, args=({'Nfeval': 0},))
    return (get_dups(tolerance), tolerance)
