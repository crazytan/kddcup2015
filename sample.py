#!/usr/bin/env python

import random

e_list = []
with open('raw/enrollment_train.csv', 'r') as fin:
    f1 = open('raw/enrollment_sample_1.csv', 'w')
    f2 = open('raw/enrollment_sample_2.csv', 'w')

    title = fin.readline()
    f1.write(title)
    f2.write(title)
    for line in fin:
        if random.uniform(0, 1) < 0.75:
            f1.write(line)
        else:
            f2.write(line)
            eid = int(line.strip().split(',')[0])
            e_list.append(eid)

    f1.close()
    f2.close()

eset = set(e_list)
with open('raw/log_train.csv', 'r') as fin:
    f1 = open('raw/log_sample_1.csv', 'w')
    f2 = open('raw/log_sample_2.csv', 'w')

    title = fin.readline()
    f1.write(title)
    f2.write(title)
    for line in fin:
        eid = int(line.strip().split(',', 1)[0])
        if eid in eset:
            f2.write(line)
        else:
            f1.write(line)

    f1.close()
    f2.close()