import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, validation_curve
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
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

def q5ToQ7Prep():
    mush_df = pd.read_csv('mushrooms.csv')
    mush_df2 = pd.get_dummies(mush_df)
    X_mush = mush_df2.iloc[:,2:]
    y_mush = mush_df2.iloc[:,1]

    # use the variables X_train2, y_train2 for Question 5
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X_mush, y_mush, random_state=0)

    # For performance reasons in Questions 6 and 7, we will create a smaller version of the
    # entire mushroom dataset for use in those questions.  For simplicity we'll just re-use
    # the 25% test split created above as the representative subset.
    #
    # Use the variables X_subset, y_subset for Questions 6 and 7.
    X_subset = X_test2
    y_subset = y_test2
    return X_train2, X_test2, y_train2, y_test2, X_subset, y_subset

def q5(X, y):
    clf = DecisionTreeClassifier(random_state=0).fit(X, y)
    df = pd.DataFrame({'Name': X.columns, 'Importance': clf.feature_importances_}).nlargest(5, 'Importance')
    return df['Name'].values.tolist()

def q6(X, y):
    gamma_range = np.logspace(-4, 1, 6)
    clf = SVC(kernel='rbf', C=1.0, random_state=0)
    train_scores, test_scores = validation_curve(clf, X, y, param_name='gamma', param_range=gamma_range,
                                                 scoring='accuracy')
    return train_scores.mean(1), test_scores.mean(1)

def q7(X, y):
    gamma_range = np.logspace(-4, 1, 6)
    train, test = q6(X, y)
    underfit_idx = np.argmin(train)
    max_train_acc_idxs = np.argwhere(train == np.max(train))
    overfit_val = np.min(test[max_train_acc_idxs])
    overfit_idx = np.argwhere(test == overfit_val)
    justright_idx = np.argmax(test)
    return gamma_range[underfit_idx], gamma_range[overfit_idx[0, 0]], gamma_range[justright_idx]

X_train2, X_test2, y_train2, y_test2, X_subset, y_subset = q5ToQ7Prep()


tr, te, jr = q7(X_subset, y_subset)
print(tr)
print(te)
print(jr)
