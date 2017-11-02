import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

cancer = load_breast_cancer()

print(cancer.DESCR) # Print the data set description
print(type(cancer.data))

cancer.keys() # dict_keys(['target_names', 'DESCR', 'data', 'target', 'feature_names'])

def q1():
    x = pd.DataFrame(cancer.target, columns=['target'])
    y = pd.DataFrame(cancer.data, columns=cancer['feature_names'])
    return pd.merge(y, x, right_index=True, left_index=True)

def q2():
    cancerdf = q1()
    malignant = len(cancerdf.where(cancerdf['target'] == 0).dropna())
    benign = len(cancerdf) - malignant
    return pd.Series([malignant, benign], index=['malignant', 'benign'])

def q3():
    cancerdf = q1()
    y = cancerdf['target']
    X = cancerdf.filter(regex=r'^(?!target)')
    return X, y

def q4():
    X, y = q3()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    return X_train, X_test, y_train, y_test

def q5():
    X_train, _, y_train, _ = q4()
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)
    return knn

def q6():
    cancerdf = q1()
    means = cancerdf.mean()[:-1].values.reshape(1, -1)
    knn = q5()
    return knn.predict(means)

def q7():
    _, X_test, _, _ = q4()
    knn = q5()
    return X_test.apply(knn.predict, axis=1).iloc[:, 0]

def q8():
    _, X_test, _, y_test = q4()
    knn = q5()
    return knn.score(X_test, y_test)
