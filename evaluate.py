#!/usr/bin/env python

from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import IO_util as io_
import map_util as mp

submission_file = open(io_.get_submission(), 'r')
pred_list = []
eid_list = []

for line in submission_file:
    eid, pred = line.strip().split(',')
    eid_list.append(int(eid))
    pred_list.append(float(pred))

y = [float(mp.truth_map[eid]) for eid in eid_list]
#truth = open("fea/train_2")
# pred = open("pred")

# y = [float(line.split(' ',1)[0]) for line in truth]
# p = [float(line) for line in pred_list]

fpr, tpr, thresholds = roc_curve(y, pred_list, pos_label=1)
# fpr, tpr, thresholds = roc_curve(y, p, pos_label=1)
print auc(fpr, tpr)
