import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, Imputer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA

def data(csvfile: str, hastarget: bool, cat_features=None):
    if cat_features is None:
        cat_features = []
    usecols = ['ticket_id', 'ticket_issued_date', 'fine_amount', 'discount_amount', 'judgment_amount'] + cat_features
    if hastarget:
        usecols.append('compliance')

    trainData = pd.read_csv(csvfile, index_col=0, parse_dates=['ticket_issued_date'], usecols=usecols)
    if hastarget:
        trainData = trainData.dropna(subset=['compliance'])
    trainData.loc[:, 'ticket_issued_date'] = trainData['ticket_issued_date'] \
        .map(lambda d: d.to_pydatetime().timestamp())

    addressesData = pd.read_csv('addresses.csv', index_col=0)
    latLonData = pd.read_csv('latlons.csv', index_col=0)
    ticketLatLonData = pd.merge(addressesData, latLonData, left_on='address', right_index=True)
    df = pd.merge(trainData, ticketLatLonData[['lat', 'lon']], left_index=True, right_index=True) # may have nans

    for feature in cat_features:
        df.loc[:, feature] = pd.Categorical(df[feature])
    return df

def traindata(cat_features=None):
    df = data('train.csv', True, cat_features)
    return df.filter(regex=r'^(?!compliance)'), df['compliance']

def testdata(cat_features=None):
    return data('test.csv', False, cat_features)

def sync_cat_data(Xtrain, Xtest, features=None):
    if features is None:
        features = []
    for feature in features:
        union = np.union1d(Xtrain[feature].cat.categories, Xtest[feature].cat.categories)
        Xtrain.loc[:, feature] = pd.Categorical(Xtrain[feature], categories=union)
        Xtest.loc[:, feature] = pd.Categorical(Xtest[feature], categories=union)

def cat2features(X):
    return pd.get_dummies(X)

def all_data(cat_features=None):
    Xtrain, ytrain = traindata(cat_features)
    Xtest = testdata(cat_features)
    sync_cat_data(Xtrain, Xtest, cat_features)
    Xtrain = cat2features(Xtrain)
    Xtest = cat2features(Xtest)
    return Xtrain, Xtest, ytrain

def feature_importance(cat_features=None):
    Xtrain, _, ytrain = all_data(cat_features)
    imputed = Imputer().fit_transform(Xtrain.values)
    scaled = MinMaxScaler().fit_transform(imputed)
    clf = DecisionTreeClassifier(max_depth=1000).fit(scaled, ytrain)
    return pd.Series(clf.feature_importances_, index=Xtrain.columns)

def pca_analysis(cat_features=None, n_components=None, svd_solver='auto'):
    Xtrain, _, _ = all_data(cat_features)
    imputed = Imputer().fit_transform(Xtrain.values)
    standardized = StandardScaler().fit_transform(imputed)
    pca = PCA(n_components=n_components, svd_solver=svd_solver).fit(standardized)
    return pca

def fit(X, y):
    param_grid = {'classifier__C': range(100, 1001, 100)}
    pipeline = Pipeline(steps=[
        ('imputer', Imputer()),
        ('scaler', MinMaxScaler()),
        ('classifier', LogisticRegression())])
    return GridSearchCV(pipeline, param_grid=param_grid, scoring='roc_auc', cv=5, verbose=10, n_jobs=-1).fit(X, y)

def predict(clf, X, index):
    predicted = clf.predict_proba(X)
    return pd.Series(predicted[:, 1], index=index, name='compliance')

def blight_model(cat_features=None):
    Xtrain, _, ytrain = all_data(cat_features)
    clf = fit(Xtrain.values, ytrain.values)
    return clf

def main():
    cat_features = ['disposition', 'violation_code']
    print(feature_importance(cat_features))
    clf = blight_model(cat_features)
    print(clf.best_score_)
    print(clf.best_params_)

if __name__ == '__main__':
    main()
