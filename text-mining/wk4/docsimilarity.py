import numpy as np
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from sklearn.metrics import accuracy_score

def convert_tag(tag):
    ''' Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets '''
    tag_dict = {
        'N': 'n',
        'J': 'a',
        'R': 'r',
        'V': 'v'
    }
    try:
        return tag_dict[tag[0]] # the first character of the nltk.pos_tag, which can be NN, VBZ, JJ, JJS, etc. 
    except KeyError:
        return None

def first(arr):
    return next(iter(arr or []), None)

def doc_to_synsets(doc):
    '''
    Returns a list of synsets in document.

    Tokenizes and tags the words in the document doc.
    Then finds the first synset for each word/tag combination.
    If a synset is not found for that combination it is skipped.

    Args:
        doc: string to be converted

    Returns:
        list of synsets

    Example:
        doc_to_synsets('Fish are nvqjp friends.')
        Out: [Synset('fish.n.01'), Synset('be.v.01'), Synset('friend.n.01')]
    '''
    tokens = nltk.word_tokenize(doc)
    return list(filter(
        lambda s: s is not None,
        [first(wn.synsets(word, convert_tag(tag))) for (word, tag) in nltk.pos_tag(tokens)]))

def similarity_score(synsets1, synsets2):
    '''
    Calculate the normalized similarity score of synsets1 onto synsets2

    For each synset in synsets1, finds the synset in synsets2 with the largest similarity value.
    Sum of all of the largest similarity values and normalize this value by dividing it by the
    number of largest similarity values found.

    Args:
        synsets1, synsets2: list of synsets from doc_to_synsets

    Returns:
        normalized similarity score of synsets1 onto synsets2

    Example:
        synsets1 = doc_to_synsets('I like cats')
        synsets2 = doc_to_synsets('I like dogs')
        similarity_score(synsets1, synsets2)
        Out: 0.73333333333333339
    '''
    return np.mean([max(s1.path_similarity(s2) or 0 for s2 in synsets2) for s1 in synsets1])

def document_path_similarity(doc1, doc2):
    """Finds the symmetrical similarity between doc1 and doc2"""

    synsets1 = doc_to_synsets(doc1)
    synsets2 = doc_to_synsets(doc2)

    return (similarity_score(synsets1, synsets2) + similarity_score(synsets2, synsets1)) / 2

def test_document_path_similarity():
    doc1 = 'This is a function to test document_path_similarity.'
    doc2 = 'Use this function to see if your code in doc_to_synsets and similarity_score is correct!'
    return document_path_similarity(doc1, doc2)

def most_similar_docs():
    paraphrases = pd.read_csv('paraphrases.csv')
    d1, d2, score = paraphrases \
        .apply(lambda r: pd.Series([r['D1'], r['D2'], document_path_similarity(r['D1'], r['D2'])]), axis=1) \
        .max() \
        .tolist()
    return d1, d2, score

def label_accuracy():
    paraphrases = pd.read_csv('paraphrases.csv')
    df = paraphrases.apply(
        lambda r: pd.Series([r['Quality'], 1 if document_path_similarity(r['D1'], r['D2']) > 0.75 else 0]),
        axis=1)
    return accuracy_score(df[0], df[1])
