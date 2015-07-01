#!/usr/bin/env python

from sklearn.datasets import *
from sklearn.cross_validation import *
from sklearn.ensemble import *
from sklearn.metrics import *
from sklearn.grid_search import GridSearchCV
import numpy as np
import IO_util as io_

def scorer(estimator, X, y):
    y_prob = np.array(estimator.predict_proba(X))
    fpr, tpr, thresholds = roc_curve(y, y_prob[:, 1], pos_label=1)
    return auc(fpr, tpr)

X, y = load_svmlight_file(io_.get_train())
y = y.astype(int)
cv = StratifiedShuffleSplit(y, n_iter=4, test_size=0.3)

params = {"n_estimators": [100],
          "max_features": ["sqrt"],
          "bootstrap": [True]
          }

# params = {"n_estimators": [100, 150, 200],
#           "max_features": ["sqrt", "log2", 10],
#           "bootstrap": [True, False]
#           }

# score_list = []

clf = GridSearchCV(RandomForestClassifier(verbose=1, n_jobs=-1),
                   scoring=scorer,
                   param_grid=params,
                   cv=cv,
                   n_jobs=-1,
                   iid=False,
                   refit=True,
                   verbose=1
                   )
clf.fit(X, y)

print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
for params, mean_score, scores in clf.grid_scores_:
    print("%0.3f (+/-%0.03f) for %r"
          % (mean_score, scores.std() * 2, params))
print()
