import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score

def data():
    df = pd.read_csv('spam.csv')
    df['target'] = np.where(df['target'] == 'spam', 1, 0)
    X = df['text']
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return X, X_train, X_test, y, y_train, y_test

def spam_balance(y):
    return np.sum(y) / len(y) * 100

def largest_token(X):
    vect = CountVectorizer().fit(X)
    longest = max(vect.vocabulary_.keys(), key=len)
    return longest

def train(X_train, X_test, y_train, y_test):
    vect = CountVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    clf = MultinomialNB(alpha=0.1).fit(X_train_vectorized, y_train)
    predictions = clf.predict(vect.transform(X_test))
    return roc_auc_score(y_test, predictions)

def q4(X):
    vect = TfidfVectorizer().fit(X)
    feature_names = vect.get_feature_names()
    X_train_vectorized = vect.transform(X)
    df = pd.DataFrame(X_train_vectorized.toarray(), columns=feature_names)
    max_tfidf = df.max().nlargest(20).reset_index().sort_values(by=[0, 'index'], ascending=[False, True]) \
        .set_index('index')
    # why max for the min tfidf? because the tfidf values of a corpus ARE df.max() of each feature.
    min_tfidf = df.max().nsmallest(20).reset_index().sort_values(by=[0, 'index']).set_index('index')
    min_tfidf.index.name = None
    max_tfidf.index.name = None
    min_tfidf[0].name = None
    max_tfidf[0].name = None
    return min_tfidf[0], max_tfidf[0]
