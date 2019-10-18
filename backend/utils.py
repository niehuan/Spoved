#去除列表中的None值
def removeNone(ur_list):
    res = []
    for val in ur_list:
        if val != None:
            res.append(val)
    return res