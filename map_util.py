import pickle
import IO_util as io_

def get_truth(key):
    return truth_map[key]

def get_user_drop(key):
    return user_drop_map.get(key, [0, 0])

def get_course_drop(key):
    return course_drop_map.get(key, [0, 0])

def get_user_id(key):
    return user_map[key]

def get_course_id(key):
    return course_map[key]

def get_obj(key):
    return object_map[key]

def get_enroll(key):
    return enroll_map[key]

def get(key):
    if key in event_map:
        return event_map[key]
    if key in category_map:
        return category_map[key]
    return [n_category - 1,]

with open("maps/truth.map", 'r') as f:
    truth_map = pickle.load(f)

with open("maps/user.map", 'r') as f:
    user_map = pickle.load(f)

with open("maps/course.map", 'r') as f:
    course_map = pickle.load(f)

with open("maps/object.map", 'r') as f:
    object_map = pickle.load(f)

with open("maps/enroll.map", 'r') as f:
    enroll_map = pickle.load(f)

event_map = {"nagivate": 0, "access": 1, "problem": 2, "page_close": 3, "discussion": 4, "video": 5, "wiki": 6}
n_event = len(event_map)

category_map = {'chapter': 1, 'course_info': 3, 'about': 0, 'sequential': 7, 'vertical': 9, 'discussion': 13, 'outlink': 5, 'static_tab': 8, 'peergrading': 12, 'course': 2, 'combinedopenended': 11, 'html': 4, 'video': 10, 'dictation': 14, 'problem': 6, 'other': 15}
# category_map = {'video': 0, 'problem': 1, 'course': 2, 'other': 3}
n_category = len(category_map)

user_drop_map = {}
course_drop_map = {}

f_enroll = open(io_.get_train_enroll(), 'r')
f_enroll.readline()
for enroll in f_enroll:
    args = enroll.strip().split(',')
    eid = int(args[0])
    user_id = user_map[args[1]]
    course_id = course_map[args[2]]

    user_cnt = get_user_drop(user_id)
    course_cnt = get_course_drop(course_id)

    if get_truth(eid) == 0:
        user_cnt[0] += 1
        course_cnt[0] += 1
    else:
        user_cnt[1] += 1
        course_cnt[1] += 1

    user_drop_map[user_id] = user_cnt
    course_drop_map[course_id] = course_cnt
