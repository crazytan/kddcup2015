#!/usr/bin/env python

from sklearn.datasets import *
from sklearn.ensemble import *
#from sklearn import neighbors
import numpy
import IO_util as io_

X_train, y_train, X_test, y_test = load_svmlight_files((io_.get_train(), io_.get_test()))

y_test = numpy.array(y_test)
print y_test.shape

classifier = RandomForestClassifier(n_estimators=100, min_samples_leaf=20, verbose=1, n_jobs=-1)
#classifier = AdaBoostClassifier(n_estimators=100)
#classifier = GradientBoostingClassifier(n_estimators=100, verbose=1)
#classifier = neighbors.KNeighborsClassifier(n_neighbors=30)
classifier.fit(X_train.toarray(), y_train)
print classifier.feature_importances_

y_prob = numpy.array(classifier.predict_proba(X_test.toarray()))
print y_prob
y_pred = y_prob[:,1]

sample_submission_file = open(io_.get_sample())
submission_file = open(io_.get_submission(),'w')
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
