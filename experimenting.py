import nltk
from nltk.corpus import brown

from nltk.corpus import stopwords
from nlpApp import status_bar
import time
import pickle

fr_stop_words = set(stopwords.words('french'))
de_stop_words = set(stopwords.words('german'))
print(de_stop_words)