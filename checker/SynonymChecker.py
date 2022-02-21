import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
stop_words = nltk.corpus.stopwords.words('english')
nltk.download('wordnet')
from nltk.corpus import wordnet
import re
import pandas as pd
import io
from sklearn.feature_extraction.text import CountVectorizer

import json
f = open('checker/wordfrequency.json')
freq_data = json.load(f)
f.close()


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def normalize_and_tokenize(text):
    text = remove_special_characters(text, remove_digits=True)
    wt = nltk.word_tokenize
    tokenized_text = wt(text=text)
    tokenized_text = [word for word in tokenized_text if word not in stop_words]

    tags = ['NNP', 'NNPS', 'PRP', 'DT', 'WP', 'WP$', 'WRB', 'UH']
    tagged_text = nltk.pos_tag(tokenized_text)

    tagged_text = [word[0] for word in tagged_text if word[1] not in tags]

    return tagged_text


def filter_words(text):  
  cv = CountVectorizer()
  cv_fit=cv.fit_transform(text)

  unique_words=cv.get_feature_names_out()
  repetitions=cv_fit.toarray().sum(axis=0)
  filtered_words = []

  for i in range(len(unique_words)):
    if(repetitions[i] > 1):
      filtered_words.append(unique_words[i])

  for i in range(len(unique_words)):
    if((freq_data.get(unique_words[i]) > 100000) and (unique_words[i] not in filtered_words)):
      filtered_words.append(unique_words[i])

  return filtered_words


from PyMultiDictionary import MultiDictionary, DICT_WORDNET
dictionary = MultiDictionary()

def find_synonyms(filtered_words):
    
  words = {}

  for word in filtered_words:
    synonyms = dictionary.synonym('en', word)
    synonyms = nltk.pos_tag(synonyms)
    tag = [nltk.pos_tag([word])[0][1]]
    synonyms = [word[0] for word in synonyms if word[1] in tag]
    words[word] = synonyms

  return words

