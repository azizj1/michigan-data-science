import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures
from matplotlib import pyplot as plt

np.random.seed(0)
n = 15
xGlobal = np.linspace(0, 10, n) + np.random.randn(n) / 5
yGlobal = np.sin(xGlobal) + xGlobal / 6 + np.random.randn(n) / 10

# X_train, X_test, y_train, y_test = train_test_split(xGlobal, yGlobal, random_state=0)

def q1(x, y):
    degrees = [1, 3, 6, 9]
    predictedValues = []

    for d in degrees:
        poly = PolynomialFeatures(degree=d)
        X_poly = poly.fit_transform(np.array(x).reshape(-1, 1))
        X_train, _, y_train, _ = train_test_split(X_poly, y, random_state=0)

        linreg = LinearRegression().fit(X_train, y_train)
        predict_poly = poly.fit_transform(np.linspace(0, 10, 100).reshape(-1, 1))
        predictedValues.append(linreg.predict(predict_poly))

    return np.array(predictedValues)

def q2(x, y):
    trainR2s = []
    testR2s = []
    for d in range(0, 10):
        poly = PolynomialFeatures(degree=d)
        X_poly = poly.fit_transform(np.array(x).reshape(-1, 1))
        X_train, X_test, y_train, y_test = train_test_split(X_poly, y, random_state=0)

        linreg = LinearRegression().fit(X_train, y_train)
        trainR2s.append(linreg.score(X_train, y_train))
        testR2s.append(linreg.score(X_test, y_test))

    return np.array(trainR2s), np.array(testR2s)

def q3(x, y):
    trainR2, testR2 = q2(x, y)
    underfitting = np.argmin(trainR2)
    overfitting = np.argmax(trainR2)
    justRight = np.argmax(testR2)
    return (underfitting, overfitting, justRight)

def q4(x, y):
    poly = PolynomialFeatures(degree=12)
    X_poly = poly.fit_transform(np.array(x).reshape(-1, 1))
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, random_state=0)
    linreg = LinearRegression().fit(X_train, y_train)
    lasreg = Lasso(alpha=0.01, max_iter=10000).fit(X_train, y_train)
    return linreg.score(X_test, y_test), lasreg.score(X_test, y_test)

train, test = q4(xGlobal, yGlobal)
print(train)
print(test)
