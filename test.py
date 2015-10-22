import time
import math
import MySQLdb
import os
import numpy as np
import dbfunc
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime

#dbfunc.Utils_decimate()
dbfunc.reset_dev()
#UtilsStr = dbfunc.Utils_List()
#print(UtilsStr)

#db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
#cur = db.cursor()
#UtilsID = '44872220'
#cur_t = time.time()
#ct = 7
#row = np.zeros(8, dtype = "double")
#str_day_array = [] #np.chararray((8, 10))
#for x in range(0, 8):
#     q_dt_end = time.time() - 86400*ct  
#     q_dt_start = time.time() - 86400*(ct+1)
#     value = datetime.datetime.fromtimestamp(q_dt_end)
#     if (x > 0):
#          str_day = value.strftime('%a')#: %m/%d')
#          str_day_array.append(str_day)
#     cur.execute("""SELECT ind, DT, Reading, M_Usage FROM Utils.scm_hist WHERE ((DT >= %s) and (DT < %s))""", (q_dt_start, q_dt_end,))
#     res = cur.fetchall()
#     if len(res) > 0:
#          rows = res[len(res)-1]
#          row[x] = rows[2]
#     else:
#          row[x] = 0
#     ct = ct - 1
#u_diff = np.zeros(7, dtype = "double")
#for x in range(0, 6):
     
#     if ((row[x] != 0) and  (row[x+1] != 0)): 
#          u_diff[x] = row[x+1] - row[x]
#     else:
#          u_diff[x] = 0
#print u_diff/100
#print str_day_array
#q_dt_start = time.mktime(time.strptime('20150909 15', '%Y%m%d %H'))
#q_dt_end = time.mktime(time.strptime('20150910 16', '%Y%m%d %H'))
#print q_dt_start
#print q_dt_end
#print "SELECT ind, DT, ID, Type, Reading FROM Utils.scm_hist WHERE ((DT >= '%s') and (DT < '%s'))" % (format(q_dt_start,'.0f'), format(q_dt_end,'.0f'),)
#cur.execute("""SELECT ind, DT, Reading, M_Usage FROM Utils.scm_hist WHERE ((DT >= %s) and (DT < %s))""", (q_dt_start, q_dt_end,))
#res = cur.fetchall()
#print res
#cnt = 0
#DT_plot = np.zeros((len(res),1), dtype = 'float')
#diff_usage = np.zeros((len(res),1), dtype = "uint8")
#print DT_plot
#print diff_usage
#if len(res) > 0:
#        for row in res :
#                print row
#                DT_plot[cnt] = row[1]
#                print row[1]
#                diff_usage[cnt] = row[3]
#                cnt = cnt + 1
#print DT_plot
#print diff_usage
#plt.figure()
#N = 7
#ind = np.arange(N)
#width = 0.4
#rects1 = plt.bar(ind, u_diff/100, width, color='g', label='kWh')
#legend = plt.legend(loc='upper right', shadow=True)
#plt.ylabel('kWh')
#plt.title('The Past 7 days of kWh Usage')
#plt.xticks(ind+width/2,str_day_array) #('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'))
#plt.xlabels( ('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun') )
#plt.plot([1,2,3,4])

#plt.xlim([0, 256])
#plt.show()
#plt.savefig("/var/www/node.png")
#dbfunc.ctrl()
#dbfunc.reset_dev()
#db.commit()
#cur.close()
#db.close()
