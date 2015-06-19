#!/usr/bin/env python

import map_util as mp
import datetime
import IO

def get_date(d):
    yy,mm,dd = d.split('-')
    return datetime.date(int(yy), int(mm), int(dd))

def extract_feature(logs):
    # feature string
    feature = ""

    # feature index
    index = 0

    # number of logs
    nlog = len(logs)

    # feature: # of logs
    feature += "%d:%d" % (index, nlog)
    index += 1

    # date list of logs
    date_list = []

    # operation count list
    cnt = [[0 for i in range(mp.n_category)] for i in range(mp.n_event)]
    # cnt = [0 for i in range(mp.n_event)]

    for log in logs:
        args = log.strip().split(',')

        # add date to list
        date_list.append(get_date(args[1].split('T')[0]))

        event_id = mp.get(args[3])
        category_id = mp.get(args[4])[0]

        cnt[event_id][category_id] += 1
        # cnt[event_id] += 1

    # feature: # of event & object category
    '''
    for eid in range(mp.n_event):
        feature += " %d:%d" % (index, cnt[eid])
        index += 1
    '''

    for eid in range(mp.n_event):
        for cid in range(mp.n_category):
            feature += " %d:%d" % (index, cnt[eid][cid])
            index += 1

    date_list = sorted(date_list)
    # feature: # of dates
    feature += " %d:%d" % (index, len(set(date_list)))
    index += 1

    # feature: time span
    feature += " %d:%d" % (index, (date_list[-1] - date_list[0]).days)
    return feature

def extract(log_file):
    f_log = open(log_file, 'r')
    f_log.readline()
    f_list = []

    prev_eid = ""
    eid = ""
    logs = []
    cnt = 0
    for log in f_log:
        cnt += 1
        log = log.strip()
        eid = log.split(',', 1)[0]
        if eid == prev_eid:
            logs.append(log)
        else:
            if len(logs) > 0:
                f_list.append((int(prev_eid), extract_feature(logs)))
            logs = [log,]
            prev_eid = eid
    f_list.append((int(eid), extract_feature(logs)))
    f_log.close()
    print "# of logs: " + str(cnt)
    return f_list

def write_feature(truth_map, feature_list, feature_file):
    f = open(feature_file, 'w')
    for feature in feature_list:
        f.write("%d %s\n" % (truth_map.get(feature[0], 0), feature[1]))
    f.close()

if __name__ == "__main__":
    print "extracting training features..."
    write_feature(mp.truth_map,
                  extract(IO.get_train_log()),
                  IO.get_train())

    print "extracting testing features..."
    write_feature({}, extract(IO.get_test_log()), IO.get_test())