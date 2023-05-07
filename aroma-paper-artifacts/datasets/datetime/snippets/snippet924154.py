import logging
import random
import threading
from datetime import datetime
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from .utils import Indexer, create_sparse, timestamp_delta_generator


def generate_indexer(user_rates_movies_ds, user_tags_movies_ds, movie_actor_ds, movie_director_ds, movie_genre_ds, movie_countries_ds, feature_begin, feature_end):
    logging.info('generating indexer ...')
    min_time = 1e+30
    max_time = (- 1)
    indexer = Indexer(['user', 'tag', 'movie', 'actor', 'director', 'genre', 'country'])
    for line in user_rates_movies_ds[1:]:
        line_items = line.split('\t')
        rating_timestamp = (float(line_items[3]) / 1000)
        min_time = min(min_time, rating_timestamp)
        max_time = max(max_time, rating_timestamp)
        rating = float(line_items[2])
        if ((feature_begin < rating_timestamp <= feature_end) and (rating > rating_threshold)):
            indexer.index('user', line_items[0])
            indexer.index('movie', line_items[1])
    for line in user_tags_movies_ds[1:]:
        line_items = line.split('\t')
        tag_timestamp = (float(line_items[3]) / 1000)
        if (feature_begin < tag_timestamp <= feature_end):
            indexer.index('user', line_items[0])
            indexer.index('movie', line_items[1])
            indexer.index('tag', line_items[2])
    for line in movie_actor_ds[1:]:
        line_items = line.split('\t')
        ranking = int(line_items[3])
        if ((ranking < actor_threshold) and (line_items[0] in indexer.mapping['movie'])):
            indexer.index('actor', line_items[1])
    for line in movie_director_ds[1:]:
        line_items = line.split('\t')
        if (line_items[0] in indexer.mapping['movie']):
            indexer.index('director', line_items[1])
    for line in movie_genre_ds[1:]:
        line_items = line.split('\t')
        if (line_items[0] in indexer.mapping['movie']):
            indexer.index('genre', line_items[1])
    for line in movie_countries_ds[1:]:
        line_items = line.split('\t')
        if (line_items[0] in indexer.mapping['movie']):
            indexer.index('country', line_items[1])
    with open('data/movielens/metadata.txt', 'w') as output:
        output.write('Nodes:\n')
        output.write('-----------------------------\n')
        output.write(('#Users: %d\n' % indexer.indices['user']))
        output.write(('#Tags: %d\n' % indexer.indices['tag']))
        output.write(('#Movies: %d\n' % indexer.indices['movie']))
        output.write(('#Actors: %d\n' % indexer.indices['actor']))
        output.write(('#Director: %d\n' % indexer.indices['director']))
        output.write(('#Genre: %d\n' % indexer.indices['genre']))
        output.write(('#Countriy: %d\n' % indexer.indices['country']))
        output.write('\nEdges:\n')
        output.write('-----------------------------\n')
        output.write(('#Rate: %d\n' % len(user_rates_movies_ds)))
        output.write(('#Attach: %d\n' % len(user_tags_movies_ds)))
        output.write(('#Played_by: %d\n' % len(movie_actor_ds)))
        output.write(('#Directed_by : %d\n' % len(movie_director_ds)))
        output.write(('#Has: %d\n' % len(movie_genre_ds)))
        output.write(('#Produced_in: %d\n' % len(movie_countries_ds)))
        output.write('\nTime Span:\n')
        output.write('-----------------------------\n')
        output.write(('From: %s\n' % datetime.fromtimestamp(min_time)))
        output.write(('To: %s\n' % datetime.fromtimestamp(max_time)))
    return indexer
