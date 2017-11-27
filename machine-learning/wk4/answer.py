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
    trainData = pd.read_csv(csvfile, index_col=0, parse_dates=['ticket_issued_date'],
                            dtype={'agency_name': 'category', 'disposition': 'category'}, usecols=usecols)
    if (hastarget):
        trainData = trainData.dropna(subset=['compliance'])
    trainData.loc[:, 'ticket_issued_date'] = trainData['ticket_issued_date'] \
        .map(lambda d: d.to_pydatetime().timestamp())

    addressesData = pd.read_csv('addresses.csv', index_col=0)
    latLonData = pd.read_csv('latlons.csv', index_col=0)
    ticketLatLonData = pd.merge(addressesData, latLonData, left_on='address', right_index=True)
    df = pd.merge(trainData, ticketLatLonData[['lat', 'lon']], left_index=True, right_index=True) # may have nans

    df.loc[:, 'agency_name'] = df['agency_name'].cat.remove_unused_categories()
    df.loc[:, 'disposition'] = df['disposition'].cat.remove_unused_categories()
    return df

def traindata():
    df = data('train.csv', True)
    return pd.get_dummies(df.filter(regex=r'^(?!compliance)')), df['compliance'].values

def testdata():
    return pd.get_dummies(data('test.csv', False))

def fit(X, y):
    param_grid = {'classifier__C': [10]}
    pipeline = Pipeline(steps=[
        ('imputer', Imputer()),
        ('scaler', MinMaxScaler()),
        ('classifier', LogisticRegression())])
    return GridSearchCV(pipeline, param_grid=param_grid, scoring='roc_auc', cv=3, n_jobs=-1).fit(X, y)

def predict(clf, X, index):
    predicted = clf.predict_proba(X)
    return pd.Series(predicted, index=index)

def execute():
    Xtrain, ytrain = traindata()
    Xtest = testdata()
    clf = fit(Xtrain, ytrain)
    print(clf.best_score_)
    return predict(clf, Xtest.values, Xtest.index)