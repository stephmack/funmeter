import math
import MySQLdb
import os
import numpy as np
import warnings
import json
import collections

def getMeterReading(NUMBER, START, STOP):
	db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
	cur = db.cursor()
	
	#try:
	#NUMBER = 42470507
	#START = 1444003200
	#STOP = 1444056735 
	query = """SELECT MIN(ind) as ind FROM scm_hist WHERE (ID = %s AND ((DT >= %s) AND (DT < %s))) union all 
	SELECT MAX(ind) as ind FROM scm_hist WHERE (ID = %s AND ((DT >= %s) AND (DT < %s)))"""
	cur.execute(query,(NUMBER,START,STOP,NUMBER,START,STOP))
	#cur.execute("""SELECT UT, MyLabel, ID  FROM Utils.utils_list""")
	res = cur.fetchall()
	#print res
	sql = """SELECT ind, DT, ID, Reading, M_Usage FROM scm_hist WHERE ind = %s"""
	#sql = """SELECT * FROM scm_hist WHERE ind = %s"""
	#res1 = cur.execute(sql,(res))

	#except:
	#        res = ""
	#print res1
	cnt = 0
	objects_list = []
	if len(res) > 0:
		for row1 in res :
        		cnt = cnt + 1
                	if cnt == 1:
                		UtilsStr = str(row1[0])
                	else:
                		UtilsStr = UtilsStr + " OR ind = " + str(row1[0])
	#print UtilsStr

	sqlvalue =  sql %(UtilsStr)
	#print sqlvalue
	cur.execute(sqlvalue)
	rows = cur.fetchall()
	#print rows
	#print rows[0][1]
	#print rows[1][1]
	for row in rows:
    		d = collections.OrderedDict()
    		d['ind'] = row[0]
    		d['DT'] = row[1]
    		d['ID'] = row[2]
    		d['Reading'] = row[3]
    		d['M_Usage'] = row[4]
    		objects_list.append(d)
 
	j = json.dumps(objects_list)
	#print j
	db.commit()      
	cur.close()        
	db.close()
	return j

def getMeterValues(number):
	db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
        cur = db.cursor()
	sql = """SELECT * FROM utils_list WHERE ID = %s"""
	cur.execute(sql,number)
        rows = cur.fetchall()
	objects_list = []
	for row in rows:
                d = collections.OrderedDict()
                d['UT'] = row[0]
                d['MyLabel'] = row[1]
                d['ID'] = row[2]
                d['price'] = row[3]
                d['CurHr'] = row[4]
		d['LstHr'] = row[5]
		d['CurDy'] = row[6]
		d['LstDy'] = row[7]
                objects_list.append(d)
	j = json.dumps(objects_list)
	
	return j
