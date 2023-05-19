import pandas as pd
from bs4 import BeautifulSoup
train_question1_tfidf = pd.read_pickle(path+'train_question1_tfidf.pkl')[:]
test_question1_tfidf = pd.read_pickle(path+'test_question1_tfidf.pkl')[:]

train_question2_tfidf = pd.read_pickle(path+'train_question2_tfidf.pkl')[:]