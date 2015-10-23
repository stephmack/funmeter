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