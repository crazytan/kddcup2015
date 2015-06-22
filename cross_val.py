#!/usr/bin/env python

from sklearn.datasets import *
from sklearn.cross_validation import *
from sklearn.ensemble import *
from sklearn.metrics import *
import numpy as np
import IO_util as io_

X, y = load_svmlight_file(io_.get_train())

y = y.astype(int)

#cv = StratifiedKFold(y, n_folds=4)
cv = StratifiedShuffleSplit(y, n_iter=4, test_size=0.3)

classifier = RandomForestClassifier(n_estimators=100, min_samples_leaf=20, verbose=1, n_jobs=-1)

score_list = []
for train, test in cv:
    probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1], pos_label=1)
    score_list.append(auc(fpr, tpr))

print score_list