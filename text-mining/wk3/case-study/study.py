import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def data():
    df = pd.read_csv('amazon-reviews.csv').dropna().query('Rating != 3')
    df['Positively Rated'] = np.where(df['Rating'] > 3, 1, 0)
    print(f"Positive to negative rating ratio: {df['Positively Rated'].mean()}")
    X = df['Reviews']
    y = df['Positively Rated']
    return X, y

def train_count(X, y, min_df=1, ngrams=None):
    if ngrams is None:
        ngrams = (1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    vect = CountVectorizer(min_df=min_df, ngram_range=ngrams).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    print(f"number of features: {X_train_vectorized.shape[0]}")
    model = LogisticRegression().fit(X_train_vectorized, y_train)
    predictions = model.predict(vect.transform(X_test))
    return model, vect, roc_auc_score(y_test, predictions)

def train_tfidf(X, y, min_df=1, ngrams=None):
    if ngrams is None:
        ngrams = (1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    vect = TfidfVectorizer(min_df=min_df, ngram_range=ngrams).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    print(f"number of features: {X_train_vectorized.shape[0]}")
    model = LogisticRegression().fit(X_train_vectorized, y_train)
    predictions = model.predict(vect.transform(X_test))
    return model, vect, roc_auc_score(y_test, predictions)

# purpose of CV is only to tell what model is better, so there's no value in returning the model. 
def count_cv(min_df=1, ngrams=None):
    if ngrams is None:
        ngrams = (1, 1)
    X, y = data()
    pipeline = Pipeline(steps=[
        ('counter', CountVectorizer(min_df=min_df, ngram_range=ngrams)),
        ('clf', LogisticRegression())])
    scores = cross_val_score(pipeline, X, y, cv=3, scoring='roc_auc')
    return scores

def tfidf_cv(min_df=1, ngrams=None):
    if ngrams is None:
        ngrams = (1, 1)
    X, y = data()
    pipeline = Pipeline(steps=[
        ('tfidf', TfidfVectorizer(min_df=min_df, ngram_range=ngrams)),
        ('clf', LogisticRegression())
    ])
    scores = cross_val_score(pipeline, X, y, cv=3, scoring='roc_auc')
    return scores

def analyze(model, vect):
    feature_names = np.array(vect.get_feature_names())
    # model.coef_ is the dimension of (1, n_features) or (n_classes, n_features)
    # find the indexes of model.coef_ in a order that will sort them
    sorted_coef_idx = model.coef_[0].argsort()
    # get from index 0 to index 10 exclusively.
    print(f"smallest coefs: {feature_names[sorted_coef_idx[:10]]}")
    # go from 0 to the last 11 exclusively, going BACKWARDS., i.e., get the last 10.
    print(f"largest coefs: {feature_names[sorted_coef_idx[:-11:-1]]}")
    print(model.predict(vect.transform(['not an issue, phone is working', 'an issue, phone is not working'])))

def count_execute(min_df=1, ngrams=None):
    X, y = data()
    model, vect, score = train_count(X, y, min_df, ngrams)
    print(score)
    analyze(model, vect)

def tfidf_execute(min_df=1, ngrams=None):
    X, y = data()
    model, vect, score = train_tfidf(X, y, min_df, ngrams)
    print(score)
    analyze(model, vect)
