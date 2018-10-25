import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
import numpy as np

df = pd.read_csv('/home/cparr/workspace/pattern_similarity/results'
                 '/pixels_labeled_drift_or_not.csv')
del df['Unnamed: 0']  # empty col, debug toolbox to cull this

# X are the features. We need to remove depth, and the labels
X = df.iloc[:, 1:-1]  # labels stored in last col and depth in first col
X = X.values
y = np.ravel(df.iloc[:, [-1]])
y = np.where(y == 'drift', 1, -1)  # encode labels to integers
#y = y.reshape(-1,1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4,
                                                    random_state=0)
pipe_rf = Pipeline([('sc', StandardScaler()),
                    ('rf', RandomForestClassifier(max_depth=10,
                                                  n_estimators=100,
                                                  oob_score=True,
                                                  n_jobs=-1))])


# pipe_rf.fit(X_train, y_train)
#
# print('Test Accuracy: %.3f' % pipe_rf.score(X_test, y_test))
# print('Train Accuracy: %.3f' % pipe_rf.score(X_train, y_train))

kfold = StratifiedKFold(n_splits=10,
                        random_state=1)

scores = []

for train, test in kfold.split(X=X, y=y):
    a = pipe_rf.fit(X[[train]], y[[train]])
    score = pipe_rf.score(X[[test]], y[[test]])
    scores.append(score)
    print(score)

print('CV Accuracy: %.3f +/- %.3f' % (np.mean(scores), np.std(scores)))

# from sklearn.model_selection import cross_val_score
# scores1 = cross_val_score(pipe_rf,
#                          X=X,
#                          y=y,
#                          cv=10,
#                          n_jobs=-1)
# print('CV Accuracy: %.3f +/- %.3f' % (np.mean(scores1), np.std(scores1)))
