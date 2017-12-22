import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

def data():
    df = pd.read_csv('spam.csv')
    df['target'] = np.where(df['target'] == 'spam', 1, 0)
    X = df['text']
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return df, X, X_train, X_test, y, y_train, y_test

def add_feature(X, feature_to_add):
    """
    Returns sparse feature matrix with added feature.
    feature_to_add can also be a list of features.
    """
    from scipy.sparse import csr_matrix, hstack
    return hstack([X, csr_matrix(feature_to_add).T], 'csr')

def q1(y):
    return np.sum(y) / len(y) * 100

def q2(X):
    vect = CountVectorizer().fit(X)
    longest = max(vect.vocabulary_.keys(), key=len)
    return longest

def q3(X_train, X_test, y_train, y_test):
    vect = CountVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    clf = MultinomialNB(alpha=0.1).fit(X_train_vectorized, y_train)
    predictions = clf.predict(vect.transform(X_test))
    return roc_auc_score(y_test, predictions)

def q4(X_train):
    vect = TfidfVectorizer().fit(X_train)
    feature_names = vect.get_feature_names()
    X_train_vectorized = vect.transform(X_train)
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

def q5(X_train, X_test, y_train, y_test):
    vect = TfidfVectorizer(min_df=3).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    clf = MultinomialNB(alpha=0.1).fit(X_train_vectorized, y_train)
    predictions = clf.predict(vect.transform(X_test))
    return roc_auc_score(y_test, predictions)

def q6(df):
    spam_length = df.query('target == 1').apply(lambda r: len(r['text']), axis=1).mean()
    notspam_length = df.query('target == 0').apply(lambda r: len(r['text']), axis=1).mean()
    return notspam_length, spam_length

def q7(X_train, X_test, y_train, y_test):
    vect = TfidfVectorizer(min_df=5).fit(X_train)
    X_train_vectorized = add_feature(vect.transform(X_train), X_train.apply(len))
    clf = SVC(C=10000).fit(X_train_vectorized, y_train)
    predictions = clf.predict(add_feature(vect.transform(X_test), X_test.apply(len)))
    return roc_auc_score(y_test, predictions)

def q8(df):
    num_digits_spam = df.query('target == 1').apply(lambda r: sum(c.isnumeric() for c in r['text']), axis=1).mean()
    num_digits_notspam = df.query('target == 0').apply(lambda r: sum(c.isnumeric() for c in r['text']), axis=1).mean()
    return num_digits_notspam, num_digits_spam

def q9(X_train, X_test, y_train, y_test):
    vect = TfidfVectorizer(min_df=5, ngram_range=(1, 3)).fit(X_train)
    X_train_vectorized = add_feature(vect.transform(X_train), [
        X_train.apply(len),
        X_train.apply(lambda s: sum(c.isnumeric() for c in s))
    ])
    clf = LogisticRegression(C=100).fit(X_train_vectorized, y_train)
    predictions = clf.predict(add_feature(vect.transform(X_test), [
        X_test.apply(len),
        X_test.apply(lambda s: sum(c.isnumeric() for c in s))
    ]))
    return roc_auc_score(y_test, predictions)

def q10(df):
    nonword_spam = df.query('target == 1').apply(lambda r: len(re.findall(r'\W', r['text'])), axis=1).mean()
    nonword_notspam = df.query('target == 0').apply(lambda r: len(re.findall(r'\W', r['text'])), axis=1).mean()
    return nonword_notspam, nonword_spam

def q11(X_train, X_test, y_train, y_test):
    vect = CountVectorizer(min_df=5, ngram_range=(2, 5), analyzer='char_wb').fit(X_train)
    feature_names = np.array(vect.get_feature_names() + ['length_of_doc', 'digit_count', 'non_word_char_count'])
    X_train_vectorized = add_feature(vect.transform(X_train), [
        X_train.apply(len),
        X_train.apply(lambda s: sum(c.isnumeric() for c in s)),
        X_train.apply(lambda s: len(re.findall(r'\W', s)))
    ])
    clf = LogisticRegression(C=100).fit(X_train_vectorized, y_train)
    predictions = clf.predict(add_feature(vect.transform(X_test), [
        X_test.apply(len),
        X_test.apply(lambda s: sum(c.isnumeric() for c in s)),
        X_test.apply(lambda s: len(re.findall(r'\W', s)))
    ]))
    score = roc_auc_score(y_test, predictions)
    sorted_index = clf.coef_[0].argsort()
    return score, feature_names[sorted_index[:10]], feature_names[sorted_index[:-11:-1]]
