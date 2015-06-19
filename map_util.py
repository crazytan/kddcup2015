import pickle

# with open("maps/user.map", 'r') as f:
#     user_map = pickle.load(f)
#
# with open("maps/course.map", 'r') as f:
#     course_map = pickle.load(f)

with open("maps/object.map", 'r') as f:
    object_map = pickle.load(f)

event_map = {"nagivate":0, "access":1, "problem":2, "page_close":3, "discussion":4, "video":5, "wiki":6}
nevent = len(event_map)

category_map = {'chapter': 1, 'course_info': 3, 'about': 0, 'sequential': 7, 'vertical': 9, 'discussion': 13, 'outlink': 5, 'static_tab': 8, 'peergrading': 12, 'course': 2, 'combinedopenended': 11, 'html': 4, 'video': 10, 'dictation': 14, 'problem': 6, 'other': 15}
ncategory = len(category_map)

def get(key):
    # if key in user_map:
    #     return user_map[key]
    # if key in course_map:
    #     return course_map[key]
    if key in object_map:
        return object_map[key]
    if key in event_map:
        return event_map[key]
    if key in category_map:
        return category_map[key]
    return [ncategory - 1,]