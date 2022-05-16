import re

import nltk
from krovetzstemmer import Stemmer
from nltk.corpus import stopwords
from unidecode import unidecode

try:
    stop_words = stopwords.words("english")
except:
    nltk.download("stopwords")
    stop_words = stopwords.words("english")


def normalize_diacritics(x):
    return unidecode(x)


def normalize_ampersand(x):
    return x.replace("&", " and ")


def acronyms_callback(x):
    return x.replace(".", "")


def strip_acronyms(x):
    x = re.sub(r"(?:[a-z]\.)+", lambda m: acronyms_callback(m.group()), x)
    x = re.sub(r"(?<=\b\w)\s*(?=\w\b)", "", x)
    return x


from string import punctuation

special_chars_trans = dict(
    [(ord(x), ord(y)) for x, y in zip(u"‘’´“”–-", u"'''\"\"--")]
)


def normalize_special_chars(x):
    return x.translate(special_chars_trans)


punctuation_string_set = punctuation.replace("&", "")
punctuation_trans = str.maketrans(
    punctuation_string_set, " " * len(punctuation_string_set)
)


def replace_punctuation(x):
    return x.translate(punctuation_trans)


def remove_saxon_genitive(x):
    return " ".join(y for y in x.split() if y != "s")


abbreviation_suffixes = ["d", "ll", "m", "re", "s", "t", "ve"]

stop_words = stop_words + abbreviation_suffixes
stop_words = set(stop_words)


def remove_stop_words(x, stopword_list):
    return " ".join(t for t in x.split() if t not in stopword_list)


stemmer = Stemmer()


def perform_stemming(x):
    return " ".join(stemmer(y) for y in x.split())


def remove_extra_whitespaces(x):
    return " ".join(x.split())


def preprocessing(x, do_stopwords_removal=True, do_stemming=True):
    x = str(x)
    x = x.lower()
    x = strip_acronyms(x)
    x = normalize_special_chars(x)
    x = replace_punctuation(x)
    x = normalize_diacritics(x)
    x = normalize_ampersand(x)
    x = remove_saxon_genitive(x)
    if do_stopwords_removal:
        x = remove_stop_words(x, stop_words)
    if do_stemming:
        x = perform_stemming(x)
    x = remove_extra_whitespaces(x)
    return x
