from sklearn.metrics import roc_curve  
from sklearn.metrics import auc  
truth = open("fea/train_2")
pred = open("pred")

y = [float(line.split(' ',1)[0]) for line in truth]
p = [float(line) for line in pred]

fpr, tpr, thresholds = roc_curve(y, p, pos_label=1)  
print auc(fpr, tpr)
