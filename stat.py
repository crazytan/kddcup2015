#!/usr/bin/env python

import pickle

if __name__ == "__main__":
    with open("maps/course.map", 'r') as f:
        course_map = pickle.load(f)

    with open("maps/user.map", 'r') as f:
        user_map = pickle.load(f)

    f_enroll = open("raw/enrollment_train.csv")
    f_truth = open("raw/truth_train.csv")
    f_enroll.readline()

    c_map = {}
    u_map = {}
    for enroll in f_enroll:
        truth = f_truth.readline()
        truth = int(truth.strip().split(',')[1])

        course_id = int(course_map[enroll.strip().split(',')[2]])
        user_id = int(user_map[enroll.strip().split(',')[1]])

        c_cnt = c_map.get(course_id, [0, 0])
        u_cnt = u_map.get(user_id, [0, 0])

        if truth == 0:
            c_cnt[0] += 1
            u_cnt[0] += 1
        else:
            c_cnt[1] += 1
            u_cnt[1] += 1

        c_map[course_id] = c_cnt
        u_map[user_id] = u_cnt

    with open("maps/course_drop.map", 'w') as f:
        pickle.dump(c_map, f)

    with open("maps/user_drop.map", 'w') as f:
        pickle.dump(u_map, f)
