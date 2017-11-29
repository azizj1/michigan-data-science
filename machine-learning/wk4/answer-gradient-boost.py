from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, Imputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
import answer as dataSource

def fit(X, y):

    # param_grid = {
    #     'classifier__n_estimators': [10, 20, 30, 40, 50, 80, 90],
    #     'classifier__learning_rate': [0.01, 0.05, 0.005],
    # }
    # param_grid = {
    #     'classifier__max_depth': range(3, 10, 2),
    #     'classifier__min_samples_split': range(200, 1001, 200)
    # }
    # param_grid = {
    #     'classifier__min_samples_leaf': range(10, 101, 10)
    # }
    # param_grid = {
    #     'classifier__max_features': [9, 'sqrt']
    # }
    param_grid = {
    }
    pipeline = Pipeline(steps=[
        ('imputer', Imputer()),
        ('scaler', MinMaxScaler()),
        ('classifier', GradientBoostingClassifier(subsample=0.8, max_depth=5, min_samples_split=1000, min_samples_leaf=10, max_features='sqrt', learning_rate=0.005, n_estimators=80))])
    return GridSearchCV(pipeline, param_grid=param_grid, scoring='roc_auc', cv=5, verbose=10, n_jobs=-1) \
                    .fit(X, y)


def blight_model(cat_features=None):
    Xtrain, _, ytrain = dataSource.all_data(cat_features)
    clf = fit(Xtrain.values, ytrain.values)
    return clf

def main():
    cat_features = ['disposition', 'violation_code', 'agency_name']
    print(dataSource.feature_importance(cat_features))
    clf = blight_model(cat_features)
    print(clf.best_score_)
    print(clf.best_params_)

if __name__ == '__main__':
    main()
