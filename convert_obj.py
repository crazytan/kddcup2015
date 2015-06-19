#!/usr/bin/env python
import pickle
import IO

obj_map = {}
category_map = {}

def retrieve(key, dic):
    if key in dic:
        res = dic[key]
    else:
        res = len(dic)
        dic[key] = res
    return res

if __name__ == "__main__":
    obj_file = IO.get_object()
    with open(obj_file, 'r') as f:
        #print
        f.readline()
        for line in f:
            args = line.strip().split(',')
            obj_map[args[1]] = (retrieve(args[2], category_map), args[3], args[4])
    with open('maps/object.map', 'w') as f:
        pickle.dump(obj_map, f)
        #pickle.dump(category_map, f)