import os
import shutil
import MySQLdb
import warnings

warnings.filterwarnings("error")

os.system('sudo git clone git://github.com/stephmack/funmeter.git')
with open('funmeter/install.csv', 'r') as f:
     for read_data in f.readlines():
     #read_data = f.readline()
     #print (read_data)
          comma_ptr = read_data.find(',')
          filename =  read_data[0:comma_ptr]
          dst = read_data[comma_ptr+1::]
          dst = dst.rstrip()
          print filename
          print dst
          shutil.copyfile('funmeter/'+filename, str(dst+"/"+filename))
f.closed
##Compile rtl_tcp
#os.chdir('/home/pi/EnergyMon/py/rtl-sdr/build')
#os.system('cmake ../ cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DINSTALL_UDEV_RULES=ON')
#os.system('make')
#os.system('sudo make install')
#os.system('sudo ldconfig')
#os.chdir('/home/pi/EnergyMon/py')
##Compile rtlamr
#os.chdir('/home/pi/src/github.com/bemasher/rtlamr')
#os.system('ls')
#os.system('sudo bash /home/pi/EnergyMon/sh/go_install.sh')
#os.chdir('/home/pi/EnergyMon/py')

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

db.commit()
cur.close()
db.close()

#clean Up
os.system('sudo rm -rf /home/pi/EnergyMon/py/funmeter')
