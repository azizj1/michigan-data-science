from nltk.corpus import words
from nltk.metrics.distance import jaccard_distance, edit_distance
from nltk.util import ngrams
import pandas as pd

def jaccard(misspelled_words, gram_number):
    correct_spellings = pd.Series(words.words())
    outcomes = []
    for entry in misspelled_words:
        words_starting_with = correct_spellings[correct_spellings.str.startswith(entry[0])]
        scoreWordPairs = [(word, jaccard_distance(
                                    set(ngrams(word, gram_number)),
                                    set(ngrams(entry, gram_number))
                                    )
                            ) for word in words_starting_with]
        closet = min(scoreWordPairs, key=lambda x: x[1])
        outcomes.append(closet[0])
    return outcomes

def edit(misspelled_words):
    correct_spellings = pd.Series(words.words())
    outcomes = []
    for entry in misspelled_words:
        words_starting_with = correct_spellings[correct_spellings.str.startswith(entry[0])]
        scoreWordPairs = [(word, edit_distance(entry, word, transpositions=False)) for word in words_starting_with]
        closet = min(scoreWordPairs, key=lambda x: x[1])
        outcomes.append(closet[0])
    return outcomes

def q9(entries=None):
    if entries is None:
        entries = ['cormulent', 'incendenece', 'validrate']
    return jaccard(entries, 3)

def q10(entries=None):
    if entries is None:
        entries = ['cormulent', 'incendenece', 'validrate']
    return jaccard(entries, 4)

def q11(entries=None):
    if entries is None:
        entries = ['cormulent', 'incendenece', 'validrate']
    return edit(entries)

def extra(entries=None):
    if entries is None:
        entries = ['cormulent', 'incendenece', 'validrate']
    return jaccard(entries, 2)

