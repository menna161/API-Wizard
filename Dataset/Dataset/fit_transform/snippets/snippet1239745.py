from io import BytesIO
import os
import requests
from zipfile import ZipFile
import numpy as np
import scipy.sparse as sp
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import LabelBinarizer
from lightfm import datasets


def get_book_crossing(min_positive_score=7, min_interactions_per_book=5, user_indicators=False, item_indicators=False, cold_start_users=False, cold_start_items=False):
    "\n    Dataset from http://www2.informatik.uni-freiburg.de/~cziegler/BX/\n\n    Improving Recommendation Lists Through Topic Diversification,\n    Cai-Nicolas Ziegler, Sean M. McNee, Joseph A. Konstan, Georg Lausen; Proceedings of the 14th International World\n    Wide Web Conference (WWW '05), May 10-14, 2005, Chiba, Japan. To appear.\n\n    :param min_positive_score:\n    :return:\n    "
    if (cold_start_items and cold_start_users):
        raise ValueError("get_book_crossing() can't return both cold_start_users and cold_start_items. Set one to False.")
    paths = _download_and_unpack_zip(url='http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip', local_path='/tmp/tensorrec/book-crossing', skip_if_not_empty=True)
    ratings = []
    with open(paths['BX-Book-Ratings.csv'], 'rb') as ratings_file:
        ratings_lines = ratings_file.readlines()
        for line in ratings_lines:
            split_line = line.decode('iso-8859-1').replace('\r', '').replace('\n', '').split('";"')
            split_line = [snip.replace('"', '') for snip in split_line]
            if (split_line[0] == 'User-ID'):
                continue
            user_id = int(split_line[0])
            isin = split_line[1]
            rating = int(split_line[2])
            rating = (1 if (rating >= min_positive_score) else 0)
            if (rating == 0):
                continue
            ratings.append((user_id, isin, rating))
    book_metadata_raw = {}
    with open(paths['BX-Books.csv'], 'rb') as books_file:
        books_lines = books_file.readlines()
        for line in books_lines:
            split_line = line.decode('iso-8859-1').replace('\r', '').replace('\n', '').split('";"')
            split_line = [snip.replace('"', '') for snip in split_line]
            if (split_line[0] == 'ISBN'):
                continue
            isbn = split_line[0]
            title = split_line[1]
            author = split_line[2]
            year = split_line[3]
            publisher = split_line[4]
            cover_url = split_line[5]
            book_metadata_raw[isbn] = (title, author, year, publisher, cover_url)
    user_metadata_raw = {}
    with open(paths['BX-Users.csv'], 'rb') as users_file:
        users_lines = users_file.readlines()
        for line in users_lines:
            split_line = line.decode('iso-8859-1').replace('\r', '').replace('\n', '').replace('NULL', '"NULL"').split('";"')
            split_line = [snip.replace('"', '') for snip in split_line]
            if (split_line[0] == 'User-ID'):
                continue
            try:
                user_id = int(split_line[0])
            except ValueError:
                continue
            location = split_line[1]
            try:
                age = split_line[2]
            except IndexError:
                continue
            user_metadata_raw[user_id] = (location, age)
    isbn_counter = {}
    for (_, isbn, _) in ratings:
        isbn_counter[isbn] = (isbn_counter.get(isbn, 0) + 1)
    ratings = [r for r in ratings if (isbn_counter[r[1]] >= min_interactions_per_book)]
    user_to_row_map = {}
    isbn_to_column_map = {}
    for (user, isbn, _) in ratings:
        if (user not in user_to_row_map):
            user_to_row_map[user] = len(user_to_row_map)
        if (isbn not in isbn_to_column_map):
            isbn_to_column_map[isbn] = len(isbn_to_column_map)
    row_to_user_map = {row: user for (user, row) in user_to_row_map.items()}
    column_to_isbn_map = {col: isbn for (isbn, col) in isbn_to_column_map.items()}
    interactions_raw = [(user_to_row_map[user], isbn_to_column_map[isbn], score) for (user, isbn, score) in ratings]
    (r, c, v) = zip(*interactions_raw)
    interactions = sp.coo_matrix((v, (r, c)), dtype=np.float64)
    user_metadata = []
    for row in range((max(row_to_user_map) + 1)):
        user = row_to_user_map[row]
        user_metadata.append(user_metadata_raw[user])
    book_metadata = []
    for col in range((max(column_to_isbn_map) + 1)):
        isbn = column_to_isbn_map[col]
        try:
            book_metadata.append(book_metadata_raw[isbn])
        except KeyError:
            book_metadata.append(('', '', '', '', ''))
    book_transformers = [('title_pipeline', Pipeline([('title_extractor', TupleExtractor(0)), ('title_vectorizer', CountVectorizer(min_df=2))])), ('author_pipeline', Pipeline([('author_extractor', TupleExtractor(1)), ('author_vectorizer', PipelineLabelBinarizer(sparse_output=True))])), ('year_pipeline', Pipeline([('year_extractor', TupleExtractor(2)), ('year_vectorizer', PipelineLabelBinarizer(sparse_output=True))])), ('publisher_pipeline', Pipeline([('publisher_extractor', TupleExtractor(3)), ('publisher_vectorizer', PipelineLabelBinarizer(sparse_output=True))]))]
    if item_indicators:
        book_transformers.append(('indicator', IndicatorFeature()))
    book_pipeline = FeatureUnion(book_transformers)
    book_features = book_pipeline.fit_transform(book_metadata)
    book_titles = [book[0] for book in book_metadata]
    user_transformers = [('location_pipeline', Pipeline([('location_extractor', TupleExtractor(0)), ('location_vectorizer', CountVectorizer(min_df=2))])), ('age_pipeline', Pipeline([('age_extractor', TupleExtractor(1)), ('age_vectorizer', PipelineLabelBinarizer(sparse_output=True))]))]
    if user_indicators:
        user_transformers.append(('indicator', IndicatorFeature()))
    user_pipeline = FeatureUnion(user_transformers)
    user_features = user_pipeline.fit_transform(user_metadata)
    if cold_start_users:
        (train_interactions, test_interactions) = _split_interactions_cold_start_users(interactions)
    elif cold_start_items:
        (train_interactions, test_interactions) = _split_interactions_cold_start_items(interactions)
    else:
        (train_interactions, test_interactions) = _split_interactions_warm_start(interactions)
    return (train_interactions, test_interactions, user_features, book_features, book_titles)
