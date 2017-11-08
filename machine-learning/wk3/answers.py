import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.dummy import DummyClassifier
from sklearn.metrics import \
    recall_score, \
    precision_score, \
    accuracy_score, \
    confusion_matrix, \
    precision_recall_curve, \
    roc_curve
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt

def init():
    df = pd.read_csv('fraud_data.csv')
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    return df, X_train, X_test, y_train, y_test

def q1(df):
    row_num = len(df)
    fraud_num = len(df[df['Class'] == 1])
    print(row_num)
    print(fraud_num)
    return fraud_num / row_num * 100

def q2(X_train, X_test, y_train, y_test):
    clf = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    recall = recall_score(y_test, clf.predict(X_test))
    return accuracy, recall

def q3(X_train, X_test, y_train, y_test):
    clf = SVC().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    return accuracy_score(y_test, y_pred), recall_score(y_test, y_pred), precision_score(y_test, y_pred)

def q4(X_train, X_test, y_train, y_test):
    clf = SVC(C=1e9, gamma=1e-07).fit(X_train, y_train)
    y_pred = (clf.decision_function(X_test) > -220).astype(np.int)
    return confusion_matrix(y_test, y_pred)

def q5(X_train, X_test, y_train, y_test):
    clf = LogisticRegression().fit(X_train, y_train)
    y_pred = clf.predict_proba(X_test)
    precision, recall, _ = precision_recall_curve(y_test, y_pred[:, 1])
    fpr, tpr, _ = roc_curve(y_test, y_pred[:, 1])

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(precision, recall)
    plt.subplot(2, 1, 2)
    plt.plot(fpr, tpr)
    plt.show()

def q6(X_train, y_train):
    grid_params = {'C': [0.01, 0.1, 1, 10, 100], 'penalty': ['l1', 'l2']}
    clf = GridSearchCV(LogisticRegression(), param_grid=grid_params, scoring='recall', cv=3).fit(X_train, y_train)
    results = clf.cv_results_['mean_test_score']
    return results.reshape(5, 2)
df, X_train, X_test, y_train, y_test = init()
print(q6(X_train, y_train))
