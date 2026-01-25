import re
import unicodedata as ud
from greek_stemmer_plus import GreekStemmer
from functools import lru_cache

stemmer = GreekStemmer()
d = {ord('\N{COMBINING ACUTE ACCENT}'):None}

# Helping function for passing the words to the stemmer using caching for better performance
@lru_cache(maxsize=200000)
def cached_stem(word):
    return stemmer.stem(word)

# processing function for text sanitazation and stemming
def text_process(text):
    # remove digits
    text = re.sub(r'[\d]+', ' ', text)
    # remove punctuation and special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    # remove word with 3 or less letters
    text = re.sub(r'\b\w{1,3}\b', ' ', text)
    # remove extra spacing
    text = re.sub(r'\s+', ' ', text)

    # stem each word
    text = ud.normalize('NFD', text).upper().translate(d)
    return " ".join(cached_stem(t) for t in text.split())

def map_stems(df):
    stem_to_word = {}

    for text in df:
        text = re.sub(r'[\d]+', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\b\w{1,3}\b', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        text = ud.normalize('NFD', text).upper().translate(d)

        for token in text.split():
            stem = cached_stem(token)
            if stem not in stem_to_word:
                stem_to_word[stem] = token
    return stem_to_word