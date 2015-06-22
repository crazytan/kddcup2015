#!/usr/bin/env python

import map_util as mp
import datetime
import IO_util

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

    # enrollment id
    eid = int(logs[0].strip().split(',', 1)[0])

    # feature: # of logs
    feature += "%d:%d" % (index, nlog)
    index += 1

    user_id, course_id = mp.get_enroll(eid)

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
    """
    for id in range(mp.n_event):
        feature += " %d:%d" % (index, cnt[id])
        index += 1

    """
    for eid in range(mp.n_event):
        feature += " %d:%d" % (index, sum(cnt[eid]))
        index += 1

        for cid in range(mp.n_category):
            feature += " %d:%d" % (index, cnt[eid][cid])
            index += 1

    date_list = sorted(date_list)
    # feature: # of dates
    feature += " %d:%d" % (index, len(set(date_list)))
    index += 1

    # feature: time span
    feature += " %d:%d" % (index, (date_list[-1] - date_list[0]).days)
    index += 1

    # # feature: # of drops in course
    # feature += " %d:%d" % (index, mp.get_course_drop(course_id)[0])
    # index += 1
    # feature += " %d:%d" % (index, mp.get_course_drop(course_id)[1])
    # index += 1

    # feature: # of drops in user
    # cnt = mp.get_user_drop(user_id)
    # if (cnt[0] + cnt[1]) > 0:
    #     feature += " %d:%.5s" % (index, float(cnt[0]) / (cnt[0] + cnt[1]))
    # else:
    #     feature += " %d:0.5" % index
    # feature += " %d:%d" % (index, mp.get_user_drop(user_id)[0])
    # index += 1
    # feature += " %d:%d" % (index, mp.get_user_drop(user_id)[1])
    # index += 1

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
                  extract(IO_util.get_train_log()),
                  IO_util.get_train())

    print "extracting testing features..."
    write_feature({}, extract(IO_util.get_test_log()), IO_util.get_test())
