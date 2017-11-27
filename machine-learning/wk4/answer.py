import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, Imputer
from sklearn.pipeline import Pipeline

def data(csvfile: str, hastarget: bool):
    usecols = ['ticket_id', 'agency_name', 'ticket_issued_date', 'disposition', 'fine_amount',
               'discount_amount', 'judgment_amount']
    if (hastarget):
        usecols.append('compliance')
    trainData = pd.read_csv(csvfile, index_col=0, parse_dates=['ticket_issued_date'], usecols=usecols)
    if (hastarget):
        trainData = trainData.dropna(subset=['compliance'])
    trainData.loc[:, 'ticket_issued_date'] = trainData['ticket_issued_date'] \
        .map(lambda d: d.to_pydatetime().timestamp())

    addressesData = pd.read_csv('addresses.csv', index_col=0)
    latLonData = pd.read_csv('latlons.csv', index_col=0)
    ticketLatLonData = pd.merge(addressesData, latLonData, left_on='address', right_index=True)
    df = pd.merge(trainData, ticketLatLonData[['lat', 'lon']], left_index=True, right_index=True) # may have nans

    df.loc[:, 'agency_name'] = pd.Categorical(df['agency_name'])
    df.loc[:, 'disposition'] = pd.Categorical(df['disposition'])
    return df

def traindata():
    df = data('train.csv', True)
    return df.filter(regex=r'^(?!compliance)'), df['compliance']

def testdata():
    return data('test.csv', False) #pd.get_dummies(data('test.csv', False))

def sync_cat_data(Xtrain, Xtest):
    agency_categories = np.union1d(Xtrain['agency_name'].cat.categories, Xtest['agency_name'].cat.categories)
    disposition_categories = np.union1d(Xtrain['disposition'].cat.categories, Xtest['disposition'].cat.categories)
    Xtrain.loc[:, 'agency_name'] = pd.Categorical(Xtrain['agency_name'], categories=agency_categories)
    Xtrain.loc[:, 'disposition'] = pd.Categorical(Xtrain['disposition'], categories=disposition_categories)
    Xtest.loc[:, 'agency_name'] = pd.Categorical(Xtest['agency_name'], categories=agency_categories)
    Xtest.loc[:, 'disposition'] = pd.Categorical(Xtest['disposition'], categories=disposition_categories)

def cat2features(X):
    return pd.get_dummies(X)

def fit(X, y):
    param_grid = {'classifier__C': [10, 20]}
    pipeline = Pipeline(steps=[
        ('imputer', Imputer()),
        ('scaler', MinMaxScaler()),
        ('classifier', LogisticRegression())])
    return GridSearchCV(pipeline, param_grid=param_grid, scoring='roc_auc', cv=3).fit(X, y)

def predict(clf, X, index):
    predicted = clf.predict_proba(X)
    return pd.Series(predicted[:, 1], index=index, name='compliance')

def execute():
    Xtrain, ytrain = traindata()
    Xtest = testdata()
    sync_cat_data(Xtrain, Xtest)
    Xtrain = cat2features(Xtrain)
    Xtest = cat2features(Xtest)
    clf = fit(Xtrain.values, ytrain.values)
    return predict(clf, Xtest.values, Xtest.index)
