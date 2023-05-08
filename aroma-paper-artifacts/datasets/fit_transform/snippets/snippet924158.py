import logging
import random
import threading
from datetime import datetime
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from .utils import Indexer, create_sparse, timestamp_delta_generator


def run(delta, observation_window, n_snapshots, censoring_ratio=0.5, single_snapshot=False):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
    with open('data/movielens/user_ratedmovies-timestamps.dat') as user_rates_movies_ds:
        user_rates_movies_ds = user_rates_movies_ds.read().splitlines()
    with open('data/movielens/user_taggedmovies-timestamps.dat') as user_tags_movies_ds:
        user_tags_movies_ds = user_tags_movies_ds.read().splitlines()
    with open('data/movielens/movie_actors.dat', encoding='latin-1') as movie_actor_ds:
        movie_actor_ds = movie_actor_ds.read().splitlines()
    with open('data/movielens/movie_directors.dat', encoding='latin-1') as movie_director_ds:
        movie_director_ds = movie_director_ds.read().splitlines()
    with open('data/movielens/movie_genres.dat') as movie_genre_ds:
        movie_genre_ds = movie_genre_ds.read().splitlines()
    with open('data/movielens/movie_countries.dat') as movie_countries_ds:
        movie_countries_ds = movie_countries_ds.read().splitlines()
    delta = timestamp_delta_generator(months=delta)
    observation_end = datetime(2009, 1, 1).timestamp()
    observation_begin = (observation_end - timestamp_delta_generator(months=observation_window))
    feature_end = observation_begin
    feature_begin = (feature_end - (n_snapshots * delta))
    indexer = generate_indexer(user_rates_movies_ds, user_tags_movies_ds, movie_actor_ds, movie_director_ds, movie_genre_ds, movie_countries_ds, feature_begin, feature_end)
    (rate_sparse, attach_sparse, played_by_sparse, directed_by_sparse, has_genre_sparse, produced_in_sparse) = parse_dataset(user_rates_movies_ds, user_tags_movies_ds, movie_actor_ds, movie_director_ds, movie_genre_ds, movie_countries_ds, feature_begin, feature_end, indexer)
    (observed_samples, censored_samples) = sample_generator(user_rates_movies_ds, observation_begin, observation_end, rate_sparse, indexer, censoring_ratio)
    (X, Y, T) = extract_features(rate_sparse, attach_sparse, played_by_sparse, directed_by_sparse, has_genre_sparse, produced_in_sparse, observed_samples, censored_samples)
    X_list = [X]
    if (not single_snapshot):
        for t in range(int((feature_end - delta)), int(feature_begin), (- int(delta))):
            (rate_sparse, attach_sparse, played_by_sparse, directed_by_sparse, has_genre_sparse, produced_in_sparse) = parse_dataset(user_rates_movies_ds, user_tags_movies_ds, movie_actor_ds, movie_director_ds, movie_genre_ds, movie_countries_ds, feature_begin, t, indexer)
            (X, _, _) = extract_features(rate_sparse, attach_sparse, played_by_sparse, directed_by_sparse, has_genre_sparse, produced_in_sparse, observed_samples, censored_samples)
            X_list = ([X] + X_list)
        for i in range(1, len(X_list)):
            X_list[i] -= X_list[(i - 1)]
    scaler = MinMaxScaler(copy=False)
    for X in X_list:
        scaler.fit_transform(X)
    X = np.stack(X_list, axis=1)
    T /= delta
    return (X, Y, T)
