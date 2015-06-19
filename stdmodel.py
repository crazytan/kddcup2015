#!/usr/bin/env python

from sklearn.datasets import *
from sklearn.ensemble import *
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import numpy
import IO

X_train, y_train, X_test, y_test = load_svmlight_files((IO.get_train(), IO.get_test()))

y_test = numpy.array(y_test)
print y_test.shape

classifier = RandomForestClassifier(n_estimators=100, min_samples_leaf=20, verbose=1, n_jobs=-1)
classifier.fit(X_train, y_train)
y_prob = numpy.array(classifier.predict_proba(X_test))
print y_prob
y_pred = y_prob[:,1]

sample_submission_file = open(IO.get_sample())
submission_file = open(IO.get_submission(),'w')
cnt = 0
for line in sample_submission_file:
    enroll_id = line.split(',')[0]
    new_line = enroll_id + ',' + str(y_pred[cnt]) + '\n'
    submission_file.write(new_line)
    cnt += 1
print cnt
sample_submission_file.close()
submission_file.close()
# print "SHAPE"
# print len(y_pred)

# fpr, tpr, thresholds = roc_curve(y_test, y_pred, pos_label=1)
# print auc(fpr, tpr)

# print clsier.score(X_test, y_test)
