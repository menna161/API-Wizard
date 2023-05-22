import logging
import networkx as nx
import numpy as np
from scipy import optimize, spatial
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors


def find_clusters(X, model, clustering_algorithm=DBSCAN(), mode='e'):
    '\n    Perform link-based cluster analysis on a knowledge graph.\n\n    The clustering happens on the embedding space of the entities and relations.\n    For example, if we cluster some entities of a model that uses :math:`k=100` (i.e. embedding space of size 100),\n    we will apply the chosen clustering algorithm on the 100-dimensional space of the provided input samples.\n\n    Clustering can be used to evaluate the quality of the knowledge embeddings, by comparing to natural clusters.\n    For example, in the example below we cluster the embeddings of international football matches and end up\n    finding geographical clusters very similar to the continents.\n    This comparison can be subjective by inspecting a 2D projection of the embedding space or objective using a\n    `clustering metric <https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation>`_.\n\n    | The choice of the clustering algorithm and its corresponding tuning will greatly impact the results.\n      Please see `scikit-learn documentation <https://scikit-learn.org/stable/modules/clustering.html#clustering>`_\n      for a list of algorithms, their parameters, and pros and cons.\n\n    Clustering is exclusive (i.e., a triple is assigned to one and only one cluster).\n\n    Parameters\n    ----------\n\n    X : ndarray, shape (n, 3) or (n)\n        The input to be clustered.\n        ``X`` can either be the triples of a knowledge graph, its entities, or its relations.\n        The argument ``mode`` defines whether ``X`` is supposed to be an array of triples\n        or an array of either entities or relations.\n    model : EmbeddingModel\n        The fitted model that will be used to generate the embeddings.\n        This model must have been fully trained already, be it directly with\n        ``fit()`` or from a helper function such as :meth:`ampligraph.evaluation.select_best_model_ranking`.\n    clustering_algorithm : object\n        The initialized object of the clustering algorithm.\n        It should be ready to apply the :meth:`fit_predict` method.\n        Please see: `scikit-learn documentation <https://scikit-learn.org/stable/modules/clustering.html#clustering>`_\n        to understand the clustering API provided by scikit-learn.\n        The default clustering model is\n        `sklearn\'s DBSCAN <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_\n        with its default parameters.\n    mode: str\n        Clustering mode.\n\n        Choose from:\n\n        - | `\'e\'` (default): the algorithm will cluster the embeddings of the provided entities.\n        - | `\'r\'`: the algorithm will cluster the embeddings of the provided relations.\n        - | `\'t\'` : the algorithm will cluster the concatenation\n            of the embeddings of the subject, predicate and object for each triple.\n\n    Returns\n    -------\n    labels : ndarray, shape [n]\n        Index of the cluster each triple belongs to.\n\n    Example\n    -------\n    >>> # Note seaborn, matplotlib, adjustText are not AmpliGraph dependencies.\n    >>> # and must therefore be installed manually as:\n    >>> #\n    >>> # $ pip install seaborn matplotlib adjustText\n    >>>\n    >>> import requests\n    >>> import pandas as pd\n    >>> import numpy as np\n    >>> from sklearn.decomposition import PCA\n    >>> from sklearn.cluster import KMeans\n    >>> import matplotlib.pyplot as plt\n    >>> import seaborn as sns\n    >>>\n    >>> # adjustText lib: https://github.com/Phlya/adjustText\n    >>> from adjustText import adjust_text\n    >>>\n    >>> from ampligraph.datasets import load_from_csv\n    >>> from ampligraph.latent_features import ScoringBasedEmbeddingModel\n    >>> from ampligraph.discovery import find_clusters\n    >>>\n    >>> # International football matches triples\n    >>> # See tutorial here to understand how the triples are created from a tabular dataset:\n    >>> # https://github.com/Accenture/AmpliGraph/blob/master/docs/tutorials/ClusteringAndClassificationWithEmbeddings.ipynb\n    >>> url = \'https://ampligraph.s3-eu-west-1.amazonaws.com/datasets/football.csv\'\n    >>> open(\'football.csv\', \'wb\').write(requests.get(url).content)\n    >>> X = load_from_csv(\'.\', \'football.csv\', sep=\',\')[:, 1:]\n    >>>\n    >>> model = ScoringBasedEmbeddingModel(eta=5,\n    >>>                                  k=300,\n    >>>                                  scoring_type=\'ComplEx\')\n    >>> model.compile(optimizer=\'adam\', loss=\'multiclass_nll\')\n    >>> model.fit(X,\n    >>>           batch_size=10000,\n    >>>           epochs=10)\n    >>>\n    >>> df = pd.DataFrame(X, columns=["s", "p", "o"])\n    >>>\n    >>> teams = np.unique(np.concatenate((df.s[df.s.str.startswith("Team")],\n    >>>                                   df.o[df.o.str.startswith("Team")])))\n    >>> team_embeddings = model.get_embeddings(teams, embedding_type=\'e\')\n    >>>\n    >>> embeddings_2d = PCA(n_components=2).fit_transform(np.array([i for i in team_embeddings]))\n    >>>\n    >>> # Find clusters of embeddings using KMeans\n    >>>\n    >>> kmeans = KMeans(n_clusters=6, n_init=100, max_iter=500)\n    >>> clusters = find_clusters(teams, model, kmeans, mode=\'e\')\n    >>>\n    >>> # Plot results\n    >>> df = pd.DataFrame({"teams": teams, "clusters": "cluster" + pd.Series(clusters).astype(str),\n    >>>                    "embedding1": embeddings_2d[:, 0], "embedding2": embeddings_2d[:, 1]})\n    >>>\n    >>> plt.figure(figsize=(10, 10))\n    >>> plt.title("Cluster embeddings")\n    >>>\n    >>> ax = sns.scatterplot(data=df, x="embedding1", y="embedding2", hue="clusters")\n    >>>\n    >>> texts = []\n    >>> for i, point in df.iterrows():\n    >>>     if np.random.uniform() < 0.1:\n    >>>         texts.append(plt.text(point[\'embedding1\']+.02, point[\'embedding2\'], str(point[\'teams\'])))\n    >>> adjust_text(texts)\n\n    .. image:: ../img/clustering/clustered_embeddings_docstring.png\n        :align: center\n\n    '
    if model.is_backward:
        model = model.model
    if (not model.is_fitted):
        msg = 'Model has not been fitted.'
        logger.error(msg)
        raise ValueError(msg)
    if (not hasattr(clustering_algorithm, 'fit_predict')):
        msg = 'Clustering algorithm does not have the `fit_predict` method.'
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
        raise ValueError(msg)
    if (mode == 't'):
        s = model.get_embeddings(X[(:, 0)], embedding_type='e')
        p = model.get_embeddings(X[(:, 1)], embedding_type='r')
        o = model.get_embeddings(X[(:, 2)], embedding_type='e')
        emb = np.hstack((s, p, o))
    else:
        emb = model.get_embeddings(X, embedding_type=mode)
    return clustering_algorithm.fit_predict(emb)
