#!/usr/bin/env python
# coding:utf-8
# 栏目循环排序

import sys
import json
import httplib
import time

accesstoken = ''
dtvsurl = ''
slaveurl = ''
columnId = 0
programids = []
totalids = []
sortedprogramids = []
sleeptime = 1

def getProgramIds():
    data = '{"label":"' + str(columnId) +'",\
    "accesstoken":"' + accesstoken + '",\
    "pagenum":1000,\
    "pageidx":1,\
    "asc":1,\
    "depth":1,\
    "matchingtype":2,\
    "sortby":10000,\
    "pagesize":500}'
    
    strRes = ''
    try :
        conn = httplib.HTTPConnection(slaveurl)
        headers = {"Content-type":"application/json;charset=utf-8"}
        conn.request("POST", "/homed/program/filter", data, headers)
        response = conn.getresponse()
        
        strRes = response.read().decode('utf-8')
        conn.close()
    except:
        print ('filter failed!')
        
    #解析返回的结果
    try:
        #print(strRes)
        result = json.loads(strRes)
        jList = result['list']
        for jItem in jList:
            programid = jItem['id']
            programids.append(programid)
            print('id=%d' %(programid))
    except:
        print("Error decode json")

def loadprogramfromFile():

    file = open("./eventIds.txt")
    while 1:
        line = file.readline()
        if not line:
            break
        line = line.strip("\r\n")
        totalids.append(line)
        print line

    print len(totalids)  
    #print(programidss)
    file.close()

def compareProgram():
    for id in totalids:
        for programid in programids:
            if programid == id:
                sortedprogramids.append(id)
                break
      
def sortProgram(programId, index):
    data = '{"accesstoken":"' + accesstoken + '",\
    "label":"' + str(columnId) + '",\
    "ids":"' + str(programId) + '",\
    "index":' + str(index) + '}'
    
    print(data)
    
    conn = httplib.HTTPConnection(dtvsurl)
    headers = {"Content-type":"application/json;charset=utf-8"}
    conn.request("POST", "/homed/program/update", data, headers)
    response = conn.getresponse()
    print(response.read().decode('utf-8'))
    conn.close()

def main():
   
    loadprogramfromFile()
    getProgramIds()
    compareProgram()
    
    count = len(sortedprogramids)
    if (0 == count):
        print('get program id list error!')
        return
    print('all program id count:%d' %(count))

    #while True:
    for id in sortedprogramids:
        sortProgram(id, count)
        time.sleep(sleeptime)
    
        
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("args must be homed_dtvs [DN dtvs] [DN slave] [accesstoken] [column id] {time(s)}")
        exit()
    else:
        dtvsurl = sys.argv[1]
        slaveurl = sys.argv[2]
        accesstoken = sys.argv[3]
        columnId = int(sys.argv[4])
        if len(sys.argv) == 6:
            sleeptime = int(sys.argv[5])
	    if sleeptime < 1:
                sleeptime = 1
    print('sleeptime =%d' %(sleeptime))
    main()
        
