import time
import math
import MySQLdb
import os
import numpy as np
import warnings
import dbfunc
import radio_rec

warnings.filterwarnings("error")

def Utils_decimate():
     db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
     cur = db.cursor()
     try:
          cur.execute("""SELECT UT, MyLabel, ID  FROM Utils.utils_list""")
          res = cur.fetchall()
     except:
          res = ""
#     print res
     if len(res) > 0:
          for row in res :
#               print row
#               print row[2]
	       UtilsID = row[2]
               cur.execute("""SELECT DT, ID, Type, Reading FROM Utils.scm WHERE ID=%s""", (UtilsID,))
               res = cur.fetchall()
               if len(res) > 0:
                    for row in res :
                         print row
                    
                    try:
                         cur.execute("""SELECT Reading FROM Utils.scm_hist WHERE ID=%s""", (UtilsID,))
                         res = cur.fetchall()
                         old_reading =  res[len(res)-1]
                         old_reading = old_reading[0]
                         meter_diff = row[3] - old_reading
                         print meter_diff
                    except:
                         meter_diff = 0
                    cur.execute("""INSERT INTO Utils.scm_hist (DT,ID,Type,Reading,M_Usage) VALUES(%s,%s,%s,%s,%s)""", (format(time.time(),'.5f'),row[1],row[2],row[3],meter_diff))
                    cur.execute("""DELETE FROM Utils.scm WHERE ID=%s""",(UtilsID))

          try:
               cur.execute("""DROP TABLE IF EXISTS scm""")
          except:
               print 'scm does not exist...'
             
          try:
               cur.execute("""CREATE TABLE IF NOT EXISTS scm(DT VARCHAR(23) DEFAULT "" NOT NULL,
               ID INT(8) DEFAULT 00 NOT NULL, Type INT(2) DEFAULT 00 NOT NULL, Tamp1 INT(2) DEFAULT 00 NOT NULL,
               Tamp2 INT(2) DEFAULT 00 NOT NULL, Reading INT(8) DEFAULT 00000000 NOT NULL)""")
          except:
               print 'scm table already exists'

     else:
          print "No Utility Meters Specified..."

          
     db.commit()
     cur.close()
     db.close()

def Utils_List():
	UtilsStr = ""

	db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
	cur = db.cursor()
	try:
        	cur.execute("""SELECT UT, MyLabel, ID  FROM Utils.utils_list""")
     		res = cur.fetchall()
	except:
      		res = ""
	print res
        cnt = 0
	if len(res) > 0:
     		for row in res :
			cnt = cnt + 1
                        if cnt == 1:
				UtilsStr = str(row[2])
			else:
          			UtilsStr = UtilsStr + "," + str(row[2])
	print UtilsStr
	db.commit()
	cur.close()
	db.close()
	return UtilsStr

def reset_dev():
     db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
     cur = db.cursor()
     try:
          cur.execute("""DROP TABLE IF EXISTS scm""")
     except:
          print 'scm table does not exist...'

     try:
          cur.execute("""CREATE TABLE IF NOT EXISTS scm(DT VARCHAR(23) DEFAULT "" NOT NULL,
          ID INT(8) DEFAULT 00 NOT NULL, Type INT(2) DEFAULT 00 NOT NULL, Tamp1 INT(2) DEFAULT 00 NOT NULL, 
          Tamp2 INT(2) DEFAULT 00 NOT NULL, Reading INT(8) DEFAULT 00000000 NOT NULL)""")
     except:
          print 'scm table already exists'

     try:
          cur.execute("""DROP TABLE IF EXISTS scm_hist1""")
     except:
          print 'scm_hist does not exist...'

     #try:
     cur.execute("""CREATE TABLE IF NOT EXISTS scm_hist1(ind INT NOT NULL AUTO_INCREMENT, DT DOUBLE DEFAULT 0.0 NOT NULL,
     ID INT(8) DEFAULT 00 NOT NULL, Type INT(2) DEFAULT 00 NOT NULL, Reading INT(8) DEFAULT 00000000 NOT NULL,
     M_Usage INT(11) DEFAULT 0 NOT NULL, PRIMARY KEY (ind))""")
     #except:
     #     print 'scm_hist table already exists'

     try:
          cur.execute("""DROP TABLE IF EXISTS utils_list1""")
     except:
          print 'utils_list does not exist...'

     try:
          cur.execute("""CREATE TABLE IF NOT EXISTS utils_list1(UT VARCHAR(3) DEFAULT "XXX" NOT
          NULL,MyLabel VARCHAR(15) DEFAULT "No Label" NOT NULL, ID INT(8) DEFAULT 00000000 NOT NULL,
          price FLOAT DEFAULT 0 NOT NULL, CurHr FLOAT DEFAULT 0 NOT NULL, LstHr FLOAT DEFAULT 0 NOT NULL,
          CurDy FLOAT DEFAULT 0 NOT NULL, LstDy FLOAT DEFAULT 0 NOT NULL)""")
     except:
          print 'utils_list table already exists'

     try:
          cur.execute("""DROP TABLE IF EXISTS ctrl1""")
     except:
          print 'ctrl does not exist...'

     try:
          cur.execute("""CREATE TABLE IF NOT EXISTS ctrl(ind INT(1) DEFAULT 1 NOT NULL, meter_update_bit INT(1) DEFAULT 0 NOT NULL,
          reset_bit INT(1) DEFAULT 0 NOT NULL, shutdown INT(1) DEFAULT 0 NOT NULL, timezone INT(11) DEFAULT 0 NOT NULL,
          ver1 VARCHAR(15) DEFAULT "1.0.0" NOT NULL, ver2 VARCHAR(15) DEFAULT "1.0.0" NOT NULL, firmup INT(1) DEFAULT 0 NOT NULL)""")
          cur.execute("""INSERT INTO Utils.ctrl (ind, meter_update_bit, reset_bit, shutdown, timezone, ver1, ver2, firmup)
          VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""", (1,0,0,0,0,'1.0.0','1.0.0',0))
     except:
          print 'utils_list table already exists'

     db.commit()
     cur.close()
     db.close()


def ctrl():
     db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
     cur = db.cursor()
     cur.execute("""SELECT * FROM Utils.ctrl""")
     res = cur.fetchall()
     row = res[0]
     #print row[0], row[1], row[2]
     if row[1] != 0:
          cur.execute("""UPDATE Utils.ctrl SET meter_update_bit = 0 WHERE ind = 1""")
          print 'Utility Number Updated...'
          #Stop rtl_tcp and rtlamr
          radio_rec.stop_radio()
          dbfunc.Utils_decimate()
          UtilsStr = dbfunc.Utils_List()
          #Start trl_tcp and rtlamr
          radio_rec.start_radio(UtilsStr)                
     
     if row[2] != 0:
          cur.execute("""UPDATE Utils.ctrl SET reset_bit = 0 WHERE ind = 1""")
          #dbfunc.reset_dev()
          print 'Device Reset...'

     if row[3] != 0:
          cur.execute("""UPDATE Utils.ctrl SET shutdown = 0 WHERE ind = 1""")
          print 'Device Shutting Down...'
          os.system('sudo halt')

     if row[7] != 0:
          cur.execute("""UPDATE Utils.ctrl SET firmup = 0 WHERE ind = 1""")
          print 'Updating Firmware'
          radio_rec.stop_radio()
          os.system('sudo python install.py')


     db.commit()
     cur.close()
     db.close()
