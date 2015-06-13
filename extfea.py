import pickle
import datetime

with open("maps/umap",'r') as f:
        usermap = pickle.load(f)
with open("maps/cmap", 'r') as f:
        coursemap = pickle.load(f)
with open("maps/omap", 'r') as f:
        objmap = pickle.load(f)
op_map = {"nagivate":0, "access":1, "problem":2, "page_close":3, "discussion":4, "video":5, "wiki":6}
op_clsnum = len(op_map)

user_st = 0
course_st = len(usermap)
obj_st = course_st + len(coursemap)

print user_st, course_st, obj_st

def todate(s):
        y,m,d = s.split('-')
        return datetime.date(int(y),int(m),int(d))
def extfea(logcol):
        args = [line.strip().split(',') for line in logcol]
        #print logcol[0]
        noperation = len(args)
        userid = int(args[0][1])
        courseid = int(args[0][2])
        objs = set([int(l[6]) for l in args])
        last_obj = int(args[-1][6])

        st_index = 0

        feastr = ""
        """
        feastr += "%d:1" % (userid+st_index,)
        st_index += len(usermap)


        feastr += " %d:1" % (courseid+st_index,)
        st_index += len(coursemap)

        feastr += "".join([" %d:1" % (objid+st_index,) for objid in sorted(objs)])
        st_index += len(objmap)
        """
        feastr += " %d:%d" % (st_index, noperation)
        st_index += 1

        op_num = [0 for i in range(op_clsnum)]
        server_op_num = [0 for i in range(op_clsnum)]
        browser_op_num = [0 for i in range(op_clsnum)]
        #1,0,0,2014-06-14T09:43:40,server,problem,4
        date_list = []
        date_set = set()
        for l in args:
                position = l[4]
                op_id = op_map[l[5]]
                logdate,logtime = l[3].split('T')
                date_list.append(logdate)

                op_num[op_id]+=1
                if(position=="server"):
                        server_op_num[op_id]+=1
                else:
                        browser_op_num[op_id]+=1

        log_times = len(set(date_list))
        start_date = todate(date_list[0])
        end_date = todate(date_list[-1])
        log_datespan = (end_date-start_date).days

        for op_id in range(op_clsnum):
                feastr += " %d:%d" % (op_id+st_index, op_num[op_id])
        st_index += op_clsnum

        for op_id in range(op_clsnum):
                feastr += " %d:%d" % (op_id+st_index, server_op_num[op_id])
        st_index += op_clsnum

        for op_id in range(op_clsnum):
                feastr += " %d:%d" % (op_id+st_index, browser_op_num[op_id])
        st_index += op_clsnum

        feastr + " %d:%d" % (st_index, log_times)
        st_index += 1

        feastr += " %d:%d" % (st_index, log_datespan)
        st_index += 1

        return feastr

def ext_file(logfile):
        fin = open(logfile,'r')

        prev_eid = ""
        col = []
        feadic = {}
        enroll_id = ""
        for line in fin:
                #print line
                enroll_id = line.split(',',1)[0]
                if enroll_id == prev_eid:
                        col.append(line)
                else:
                        #print enroll_id, len(col)
                        #raw_input()
                        if(len(col)>0):
                                feastr = extfea(col)
                                feadic[int(prev_eid)] = feastr
                        col = [line,]
                        prev_eid = enroll_id
        feastr = extfea(col)
        feadic[int(enroll_id)] = feastr
        fin.close()

        return feadic

def write_train(truthfile,feadic,outputfile):
        tf = open(truthfile)
        train = open(outputfile,'w')

        for line in tf:
                eid, res = line.strip().split(',')
                if int(eid) not in feadic:
                        print eid
                        continue
                feastr = feadic[int(eid)]
                train.write("%s %s\n" % (res, feastr))
        tf.close()
        train.close()

def write_test(testfile, feadic, outputfile):
        tf = open(testfile)
        test = open(outputfile,'w')
        for line in tf:
                eid, remain = line.strip().split(',',1)
                if int(eid) not in feadic:
                        print eid
                        continue
                feastr = feadic[int(eid)]
                test.write("0 %s\n" % feastr)
        tf.close()
        test.close()

if __name__=="__main__":
        feadic = ext_file("clean/log_train.csv",)
        write_train("clean/truth_train.csv", feadic, "feature/train")

        feadic = ext_file("clean/log_test.csv")
        write_test("clean/enrollment_test.csv", feadic, "feature/test")
