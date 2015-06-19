#!/usr/bin/env python

import pickle

course_map = {}
user_map = {}
obj_map = {}

enrollment_user_course = {}

def retrieve(key, dic):
    if key in dic:
        res = dic[key]
    else:
        res = len(dic)
        dic[key] = res
    return res

def clean_enroll(fn):
    print fn
    fin = open("raw/"+fn,'r')
    fout = open("clean/"+fn,'w')

    fin.readline()
    for row in fin:
        arg = row.strip().split(',')
        user_index = retrieve(arg[1], user_map)
        course_index = retrieve(arg[2], course_map)
        fout.write("%s,%d,%d\n" % (arg[0], user_index, course_index))
        enrollment_user_course[arg[0]] = (user_index,course_index)
    fin.close()
    fout.close()

def clean_log(fn):
    print fn
    fin = open("raw/"+fn,'r')
    fout = open("clean/"+fn,'w')

    fin.readline()
    for row in fin:
        arg = row.strip().split(',')
        #enrollment_id,username,course_id,time,source,event,object
        fout.write("%s,%d,%d,%s,%s,%s,%d\n" % (arg[0], enrollment_user_course[arg[0]][0],
                                               enrollment_user_course[arg[0]][1], arg[1], arg[2], arg[3], retrieve(arg[4], obj_map)))
    fin.close()
    fout.close()

if __name__=="__main__":
    clean_enroll("enrollment_train.csv")
    clean_log("log_train.csv")
    clean_enroll("enrollment_test.csv")
    clean_log("log_test.csv")
    with open("maps/user.map",'w') as f:
        pickle.dump(user_map, f)
    with open("maps/course.map", 'w') as f:
        pickle.dump(course_map, f)
    with open("maps/object.map", 'w') as f:
        pickle.dump(obj_map, f)
