import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
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

ans = q1(xGlobal, yGlobal)
print(ans)
print(ans.shape)
