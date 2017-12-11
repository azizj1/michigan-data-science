import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import numpy as np

def data():
    with open('moby.txt', 'r') as file:
        moby_raw = file.read()
    tokens = nltk.word_tokenize(moby_raw)
    text = nltk.Text(tokens)
    sentences = nltk.sent_tokenize(moby_raw)
    return tokens, text, sentences

def num_tokens(tokens):
    return len(tokens) # or len(text)

def num_unique_tokens(tokens):
    return len(set(tokens)) # or len(set(text))

# unique tokens after lemmatizing the VERBS
def lem_verbs_count(text):
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w, 'v') for w in text] # 'v' for verbs
    return len(set(lemmatized))

def q1(tokens):
    return num_unique_tokens(tokens) / num_tokens(tokens)

def q2(tokens):
    pattern = re.compile('^[wW]hale$')
    filtered_count = len(list(filter(pattern.match, tokens)))
    return filtered_count / len(tokens) * 100

def q3(text):
    freq = FreqDist(text)
    return freq.most_common()[:20]

def q4(text):
    freq = FreqDist(text)
    return sorted([word for word in freq.keys() if len(word) > 5 and freq[word] > 150])

def q5(tokens):
    word = max(tokens, key=len)
    return word, len(word)

def q6_wrong(text):
    freq = FreqDist(text)
    return next(iter([word for word in freq.keys() if word.isalpha()] or []), None)

def q6(text):
    freq = FreqDist(text)
    return list(map(lambda t: (t[1], t[0]), filter(lambda x: x[0].isalpha() and x[1] > 2000, freq.most_common())))

def q7(sentences):
    return np.mean([len(nltk.word_tokenize(sent)) for sent in sentences])

def q8(tokens):
    return FreqDist(tag for (word, tag) in nltk.pos_tag(tokens)).most_common()[:5]
