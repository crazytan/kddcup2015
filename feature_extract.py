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
    cnt = [[0 for i in range(mp.ncategory)] for i in range(mp.nevent)]

    for log in logs:
        args = log.strip().split(',')

        # add date to list
        date_list.append(get_date(args[1].split('T')[0]))

        event_id = mp.get(args[3])
        category_id = mp.get(args[4])[0]

        cnt[event_id][category_id] += 1

    # feature: # of event & object category
    for eid in range(mp.nevent):
        for cid in range(mp.ncategory):
            feature += " %d:%d" % (index, cnt[eid][cid])
            index += 1

    date_list = sorted(date_list)
    # feature: # of dates
    feature += " %d:%d" % (index, len(date_list))
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
                f_list.append((int(eid), extract_feature(logs)))
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

def get_truth_map(truth_file):
    t_map = {}
    f_truth = open(truth_file, 'r')
    for line in f_truth:
        eid, status = line.strip().split(',')
        t_map[int(eid)] = int(status)
    f_truth.close()
    return t_map

if __name__ == "__main__":
    print "extracting training features..."
    write_feature(get_truth_map(IO.get_train_truth()),
                  extract(IO.get_train_log()),
                  "feature/train")

    print "extracting testing features..."
    write_feature({}, extract(IO.get_test_log()), "feature/test")