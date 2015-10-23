import os
import shutil
import MySQLdb
import warnings

warnings.filterwarnings("error")
db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
cur = db.cursor()

#try:
#     cur.execute("""CREATE DATABASE IF NOT EXISTS Utils""")
#except:
#     print 'Utils database already exists'

#check scm table
try:
     cur.execute("""CREATE TABLE IF NOT EXISTS scm(DT VARCHAR(23) DEFAULT "" NOT NULL,
          ID INT(8) DEFAULT 00 NOT NULL, Type INT(2) DEFAULT 00 NOT NULL, Tamp1 INT(2) 
          DEFAULT 00 NOT NULL,
          Tamp2 INT(2) DEFAULT 00 NOT NULL, Reading INT(8) DEFAULT 00000000 NOT NULL)""")
except:
     print 'scm table already exists'

#check scm_hist table
try: 
     cur.execute("""CREATE TABLE IF NOT EXISTS scm_hist(ind INT NOT NULL AUTO_INCREMENT, 
     DT DOUBLE DEFAULT 0.0 NOT NULL,
     ID INT(8) DEFAULT 00 NOT NULL, Type INT(2) DEFAULT 00 NOT NULL, Reading INT(8) DEFAULT 
     00000000 NOT NULL, M_Usage INT(11) DEFAULT 0 NOT NULL, PRIMARY KEY (ind))""")

except:
     print 'scm_hist table already exists'

#Check utils_list table
try:
     cur.execute("""CREATE TABLE IF NOT EXISTS utils_list(UT VARCHAR(3) DEFAULT "XXX" NOT 
     NULL,MyLabel VARCHAR(15) DEFAULT "No Label" NOT NULL, ID INT(8) DEFAULT 00000000 NOT NULL,
     price FLOAT DEFAULT 0 NOT NULL, CurHr FLOAT DEFAULT 0 NOT NULL, LstHr FLOAT DEFAULT 0 NOT NULL,
     CurDy FLOAT DEFAULT 0 NOT NULL, LstDy FLOAT DEFAULT 0 NOT NULL)""")

except:
     print 'utils_list table already exists'


try: 
     cur.execute("""CREATE TABLE IF NOT EXISTS ctrl(ind INT(1) DEFAULT 1 NOT NULL, meter_update_bit INT(1) DEFAULT 0 NOT NULL,
     reset_bit INT(1) DEFAULT 0 NOT NULL, shutdown INT(1) DEFAULT 0 NOT NULL, timezone INT(11) DEFAULT 0 NOT NULL,
     ver VARCHAR(15) DEFAULT "1.0.0" NOT NULL, firmup INT(1) DEFAULT 0 NOT NULL)""")
     cur.execute("""INSERT INTO Utils.ctrl (ind, meter_update_bit, reset_bit, shutdown, timezone, ver, firmup) 
     VALUES(%s,%s,%s,%s,%s,%s,%s)""", (1,0,0,0,0,'1.0.0',0))
except:
     print 'ctrl table already exists'

with open('../ver/ver.txt', 'r') as f:
     ver = f.readlines()
     ver1 = str(ver[0])
     ver1 = ver1.rstrip()
     print ver1
     try:
          cur.execute("""UPDATE Utils.ctrl SET ver1 = %s WHERE ind = 1""",(ver))
     except:
          print 'Could not Update "ver"'

db.commit()
cur.close()
db.close()
