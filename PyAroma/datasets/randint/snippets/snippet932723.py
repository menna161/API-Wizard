import spacy
import csv
import re
import ray
import multiprocessing
from tqdm import tqdm
from itertools import chain
from random import shuffle, randint


def generate_encoded_text(self, row):
    nlp = self.nlp
    pattern = self.pattern
    category = (re.sub(pattern, '-', row[self.category_field].lower().strip()) if (self.category_field is not None) else None)
    title = (row[self.title_field] if (self.title_field is not None) else None)
    body = (row[self.body_field] if (self.body_field is not None) else None)
    if (self.keywords_field is None):
        text = re.sub(u'[‘’]', "'", re.sub(u'[“”]', '"', row[self.keyword_gen]))
        doc = nlp(text)
        keywords_pos = [(chunk.text if (chunk.pos_ == 'NOUN') else (chunk.lemma_ if (chunk.pos_ in ['VERB', 'ADJ', 'ADV']) else 'I')) for chunk in doc if (not chunk.is_stop)]
        keywords_ents = [re.sub(' ', '-', chunk.text) for chunk in doc.ents]
        keywords_compounds = [re.sub(' ', '-', chunk.text) for chunk in doc.noun_chunks if (len(chunk.text) < self.keyword_length_max)]
        keywords = list((set(((keywords_pos + keywords_ents) + keywords_compounds)) - self.PRONOUNS))
    else:
        keywords = [keyword.strip() for keyword in row[self.keywords_field].split(self.keyword_sep)]
        keywords = list(set(keywords))
    encoded_texts = []
    for _ in range(self.repeat):
        new_keywords = keywords
        shuffle(new_keywords)
        new_keywords = ' '.join(new_keywords[:randint(0, self.max_keywords)])
        encoded_texts.append(((((((self.start_token + self.build_section('category', category)) + self.build_section('keywords', new_keywords)) + self.build_section('title', title)) + self.build_section('body', body)) + self.end_token) + '\n'))
    return encoded_texts
