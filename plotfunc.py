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
import calendar

def plot_seven():
#if (1):
      db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
      cur = db.cursor()
      try:
           cur.execute("""SELECT UT, MyLabel, ID, price, month FROM Utils.utils_list""")
           res = cur.fetchall()
      except:
           res = ""
      cnt = 0
      if len(res) > 0:
           for row in res :
                 UtilsID = row[2]
                 UtilsName = row[0]
                 price = row[3]
                 metername = row[1]
		 month = row[4]
                 cur.execute("""SELECT timezone FROM Utils.ctrl""")
                 res = cur.fetchall()
                 timezone = res[0]
                 print timezone[0]
                 cur_t = time.time()
                 ct = 6
                 row1 = np.zeros(8, dtype = "double")
                 row2 = np.zeros(8, dtype = "double")
                 str_day_array = [] #np.chararray((8, 10))
                 for x in range(0, 7):
                      q_dt_end = time.time() - (86400*ct) + (3600*timezone[0])
                      q_dt_start = time.time() - (86400*(ct+1)) + (3600*timezone[0])
                      value = datetime.datetime.fromtimestamp(q_dt_end)
                      #value1 = datetime.datetime.fromtimestamp(q_dt_start)
                      str_start = value.strftime('%m%d%Y 00:00:00')
                      str_end = value.strftime('%m%d%Y 23:59:59')
                      start_time = time.mktime(time.strptime(str_start, '%m%d%Y %H:%M:%S')) - 3600*timezone[0] 
                      end_time = time.mktime(time.strptime(str_end, '%m%d%Y %H:%M:%S')) - 3600*timezone[0]
		      value = datetime.datetime.fromtimestamp(q_dt_end)# + 3600*timezone[0])
                      str_day = value.strftime('%m/%d') #%a
                      str_day_array.append(str_day)
                      #value1 = datetime.datetime.fromtimestamp(start_time)
		      #str_day1 = value1.strftime('%m/%d')
                      #value2 = datetime.datetime.fromtimestamp(end_time)
                      #str_day2 = value2.strftime('%m/%d')
		      #print value1, value2
 		      cur.execute("""SELECT ind, DT, Reading, M_Usage FROM Utils.scm_hist WHERE (((DT >= %s) and (DT < %s)) and ID=%s)""", (start_time, end_time, UtilsID))
                      res = cur.fetchall()
                      if len(res) > 0:
                           rows1 = res[len(res)-1]
                           rows2 = res[0] 
                           row1[x] = rows1[2]
                           row2[x] = rows2[2]    
                      else:
                           row1[x] = 0
                           row2[x] = 0
                      ct = ct - 1
                 u_diff = np.zeros(7, dtype = "double")
                 for x in range(0, 7):
                      #if ((row2[x] != 0) and  (row1[x] != 0)):
                      u_diff[x] = row1[x] - row2[x]
                      #else:
                      #     u_diff[x] = 0
                 print u_diff/100
                 print str_day_array     
		 if (month == 0):
 		      cur.execute("""UPDATE Utils.utils_list SET CurDy = %s WHERE ID = %s""", (u_diff[6], UtilsID))
		      cur.execute("""UPDATE Utils.utils_list SET LstDy = %s WHERE ID = %s""", (u_diff[5], UtilsID))
                 plt.figure(figsize=(4,3))
                 matplotlib.rcParams.update({'font.size': 8})
                 N = 7
                 ind = np.arange(N)
                 width = 0.4
                 if UtilsName[0] == 'E':
                      rects1 = plt.bar(ind, u_diff/100, width, color='g', label='kWh')
                      legend = plt.legend(loc='upper left', shadow=True)
		      for rect in rects1:
		           height = rect.get_height()
                           plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '$%.2f'%float(height*price),
                	   ha='center', va='bottom')
                      x1,x2,y1,y2 = plt.axis()
		      plt.axis((x1-.5,x2,y1,y2+12))
                      plt.ylabel('kWh') 
		      cur_time = datetime.datetime.fromtimestamp(time.time() + 3600*timezone[0])
                      str_day = cur_time.strftime('%m/%d/%Y %H:%M:%S')
                      #plt.xlabel('Hours (Local) - Generated: '+ str_day)
		      plt.xlabel('Generated: ' + str_day)
                      plt.title(metername+': kWh Usage ($'+str(format((u_diff.sum()/100)*price, '.2f'))+')')
                      plt.xticks(ind+width/2,str_day_array)
                      plt.show()
                      plt.savefig("/var/www/seven_days_"+str(UtilsName)+"_"+str(UtilsID)+".png")
                 elif UtilsName[0] == 'G':
 		      rects1 = plt.bar(ind, u_diff/100, width, color='g', label='CCF')
                      legend = plt.legend(loc='upper left', shadow=True)
                      for rect in rects1:
                           height = rect.get_height()
                           plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '$%.2f'%float(height*price),
                           ha='center', va='bottom')
		      x1,x2,y1,y2 = plt.axis()
                      plt.axis((x1-.5,x2,y1,y2+12))
                      plt.ylabel('CCF')
                      plt.xlabel('Date')
                      plt.title('The Past 7 days of CCF Usage ($'+str(format((u_diff.sum()/100)*price, '.2f'))+')')
                      plt.xticks(ind+width/2,str_day_array)
                      plt.show()
                      plt.savefig("/var/www/seven_days_"+str(UtilsName)+"_"+str(UtilsID)+".png")
      db.commit()
      cur.close()
      db.close()

def plot_hour():
#if (1):
      db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
      cur = db.cursor()
      try:
           cur.execute("""SELECT UT, MyLabel, ID, price FROM Utils.utils_list""")
           res = cur.fetchall()
      except:
           res = ""
      if len(res) > 0:
           for row in res :
                 UtilsID = row[2]
                 UtilsName = row[0]
 		 price = row[3]
                 metername = row[1]
  		 cur.execute("""SELECT timezone FROM Utils.ctrl""")
                 res = cur.fetchall()
                 timezone = res[0]
                 print timezone[0]
                 cur_t = time.time()
                 row1 = np.zeros(8, dtype = "double")
                 row2 = np.zeros(8, dtype = "double")
                 str_day_array = [] #np.chararray((8, 10))
                 q_dt_end = time.time()
                 q_dt_start = time.time() - 3600
                 value = datetime.datetime.fromtimestamp(q_dt_end)
                 value1 = datetime.datetime.fromtimestamp(q_dt_start)
                 str_start = value1.strftime('%m%d%Y %H:%M:%S')
                 str_end = value.strftime('%m%d%Y %H:%M:%S')
                 start_time = time.mktime(time.strptime(str_start, '%m%d%Y %H:%M:%S'))
                 end_time = time.mktime(time.strptime(str_end, '%m%d%Y %H:%M:%S'))
                 #str_day = value.strftime('%H:%M') #%a
                 #str_day_array.append(str_day)
                 cur.execute("""SELECT ind, DT, Reading, M_Usage FROM Utils.scm_hist WHERE (((DT >= %s) and (DT < %s)) and ID=%s)""", (q_dt_start, q_dt_end, UtilsID))
                 res = cur.fetchall()
                 cnt=0                  
		 str_hr_array = []
                 diff = np.zeros(len(res), dtype = "double")
 		 DT = np.zeros(len(res), dtype = "double")
                 if len(res) > 0:
 		      for row in res:
                           DT[cnt] = row[1]
                           temp = row[1]
			   value = datetime.datetime.fromtimestamp(temp+(timezone[0]*3600))
			   str_hr = value.strftime('%H') #%a
                           str_hr_array.append(str_hr)
                  	   diff[cnt] = row[2]
                           cnt = cnt + 1
                 print str_hr_array
                 print diff
                 plt.figure(figsize=(4,3))
                 matplotlib.rcParams.update({'font.size': 8})
                 N = len(diff)
                 ind = np.arange(N)
                 width = 0.4
                 if UtilsName[0] == 'E':
		      try:
                           rects1 = plt.plot((DT-start_time)/60, (diff-diff[0])/100, 's-',label='kWh')
                      except:
		           rects1 = plt.plot(0, 0, 's-',label='kWh')
			   str_hr = '0'
		      legend = plt.legend(loc='upper left', shadow=True)
                      plt.ylabel('kWh')
		      cur_time = datetime.datetime.fromtimestamp(time.time() + 3600*timezone[0])
                      str_day1 = cur_time.strftime('%m/%d/%Y %H:%M:%S')
                      #plt.xlabel('Hours (Local) - Generated: '+ str_day)
		      plt.xlabel('Past Hour - Generated: '+ str_day1)
                      plt.title(metername+': Past Hour')
                      #plt.xticks(N,str_hr_array)
                      plt.show()
                      plt.savefig("/var/www/one_hour_"+str(UtilsName)+"_"+str(UtilsID)+".png")
                 elif UtilsName[0] == 'G':
                      try:
		           rects1 = plt.plot((DT-start_time)/60, diff-diff[0], 's-',label='CCF')
                      except:
		           rects1 = plt.plot(0, 0, 's-',label='CCF')
			   str_hr = '0'     
    		      legend = plt.legend(loc='upper right', shadow=True)
                      plt.ylabel('CCF')
                      plt.xlabel('Minutes Past '+str_hr+':00 Hours')
                      plt.title(metername+': Hour '+str_hr+':00')
                      plt.show()
                      plt.savefig("/var/www/one_hour_"+str(UtilsName)+"_"+str(UtilsID)+".png")
      db.commit()
      cur.close()
      db.close()

def plot_day():
#if (1):
      db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
      cur = db.cursor()
      try:
           cur.execute("""SELECT UT, MyLabel, ID, price, month FROM Utils.utils_list""")
           res = cur.fetchall()
      except:
           res = ""
      cnt = 0
      if len(res) > 0:
           for row in res :
                 UtilsID = row[2]
                 UtilsName = row[0]
  		 price = row[3]
                 metername = row[1]
		 month = row[4]
                 cur.execute("""SELECT timezone FROM Utils.ctrl""")
                 res = cur.fetchall()
                 timezone = res[0]
                 print timezone[0]
                 cur_t = time.time()
                 ct = 23
                 row1 = np.zeros(24, dtype = "double")
                 row2 = np.zeros(24, dtype = "double")
                 str_day_array = [] #np.chararray((8, 10))
                 for x in range(0, 24):
                      q_dt_end = time.time() - 3600*ct
                      q_dt_start = time.time() - 3600*(ct+1)
                      value = datetime.datetime.fromtimestamp(q_dt_end+(timezone[0]*3600))
                      value1 = datetime.datetime.fromtimestamp(q_dt_end)
                      str_start = value1.strftime('%m%d%Y %H:00:00')
                      str_end = value1.strftime('%m%d%Y %H:59:59')
                      #start_time = time.mktime(time.strptime(q_dt_start, '%m%d%Y %H:%M:%S'))
                      #end_time = time.mktime(time.strptime(q_dt_end, '%m%d%Y %H:%M:%S'))
		      start_time = time.mktime(time.strptime(str_start, '%m%d%Y %H:%M:%S'))
                      end_time = time.mktime(time.strptime(str_end, '%m%d%Y %H:%M:%S'))
                      str_day = value.strftime('%H') #%a
                      str_day_array.append(str_day)
                      cur.execute("""SELECT ind, DT, Reading, M_Usage FROM Utils.scm_hist WHERE (((DT >= %s) and (DT < %s)) and ID=%s)""",(start_time, end_time, UtilsID))
                      res = cur.fetchall()
                      if len(res) > 0:
                           rows1 = res[len(res)-1]
                           rows2 = res[0]
                           row1[x] = rows1[2]
                           row2[x] = rows2[2]
                      else:
                           row1[x] = 0
                           row2[x] = 0
                      ct = ct - 1
                 u_diff = np.zeros(24, dtype = "double")
                 for x in range(0, 24):
                      #if ((row2[x] != 0) and  (row1[x] != 0)):
                      u_diff[x] = row1[x] - row2[x]
                      #else:
                      #     u_diff[x] = 0
                 print u_diff/100
                 print str_day_array
		 if (month == 0):
		      cur.execute("""UPDATE Utils.utils_list SET CurHr = %s WHERE ID = %s""", (u_diff[23], UtilsID))
                      cur.execute("""UPDATE Utils.utils_list SET LstHr = %s WHERE ID = %s""", (u_diff[22], UtilsID))
		 plt.figure(figsize=(6,3))
                 matplotlib.rcParams.update({'font.size': 7})
                 N = 24
                 ind = np.arange(N)
                 width = 0.4
                 if UtilsName[0] == 'E':
                      rects1 = plt.bar(ind, u_diff/100, width, color='g', label='kWh')
                      legend = plt.legend(loc='upper left', shadow=True)
		      #x1,x2,y1,y2 = plt.axis()
                      #plt.axis((x1-.75,x2-.75,y1,y2))
                      plt.ylabel('kWh')
		      cur_time = datetime.datetime.fromtimestamp(time.time() + 3600*timezone[0])
                      str_day = cur_time.strftime('%m/%d/%Y %H:%M:%S')
                      plt.xlabel('Hours (Local) - Generated: '+ str_day)
                      plt.title(metername+': 24 hrs of kWh Usage ($'+str(format((u_diff.sum()/100)*price, '.2f'))+')')
                      plt.xticks(ind+width/2,str_day_array)
		      ax2 = plt.twinx()
		      ax2.plot(ind+(width/2), (u_diff/100)*price, 's-b')
                      ax2.set_ylabel('$/hr', color='b')
		      for tl in ax2.get_yticklabels():
		           tl.set_color('b')
		      x1,x2,y1,y2 = ax2.axis()
                      ax2.axis((x1-.75,x2-.75,y1,y2))
                      plt.xticks(ind+width/2,str_day_array)
  		      plt.show()
                      plt.savefig("/var/www/one_day_"+str(UtilsName)+"_"+str(UtilsID)+".png")

      	         elif UtilsName[0] == 'G':
                      rects1 = plt.bar(ind, u_diff/100, width, color='g', label='CCF')
                      legend = plt.legend(loc='upper left', shadow=True)
                      plt.ylabel('CCF')
 		      plt.xlabel('Hour')
                      plt.title(metername+': 24 hrs of CCF Usage ($'+str(format((u_diff.sum()/100)*price, '.2f'))+')')
                      plt.xticks(ind+width/2,str_day_array)
		      for tl in ax2.get_yticklabels():
                           tl.set_color('b')
                      x1,x2,y1,y2 = plt.axis()
                      plt.axis((x1-.75,x2-.75,y1,y2))
                      plt.xticks(ind+width/2,str_day_array)
		      plt.show()
                      plt.savefig("/var/www/one_day_"+str(UtilsName)+"_"+str(UtilsID)+".png")
      db.commit()
      cur.close()
      db.close()

def plot_month():
#if (1):
      db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
      cur = db.cursor()
      try:
           cur.execute("""SELECT UT, MyLabel, ID, price, month FROM Utils.utils_list""")
           res = cur.fetchall()
      except:
           res = ""
      cnt = 0
      if len(res) > 0:
           for row in res :
                 UtilsID = row[2]
                 UtilsName = row[0]
                 price = row[3]
                 metername = row[1]
                 month = row[4]
                 cur.execute("""SELECT timezone FROM Utils.ctrl""")
                 res = cur.fetchall()
                 timezone = res[0]
                 cur_t = time.time()
                 row1 = np.zeros(12, dtype = "double")
                 row2 = np.zeros(12, dtype = "double")
		 u_diff = np.zeros(12, dtype = "double")
		 u_diff1 = np.zeros(12, dtype = "double")
                 str_day_array = [] #np.chararray((8, 10))
                 cur_dt = time.time() + (3600*timezone[0])
		 value = datetime.datetime.fromtimestamp(cur_dt)
		 str_m = value.strftime('%m')
		 str_y = value.strftime('%y')
                 value = datetime.datetime.fromtimestamp(cur_dt)
		 cur_month = value.month
		 if cur_month == 12:
		      cur_year = value.year
		      cur_month = 1
		 else:
		      cur_year = value.year - 1		 
		      cur_month = value.month + 1
		 print cur_month, cur_year
		 for x in range(0, 12): 
		      numdays = calendar.monthrange(cur_year,cur_month)[1]
		      str_start = value.strftime(str(cur_month)+ '1'+ str(cur_year) + ' 00:00:00')
		      str_end = value.strftime(str(cur_month)+ str(numdays) + str(cur_year) + ' 23:59:59')
		      start_time = time.mktime(time.strptime(str_start, '%m%d%Y %H:%M:%S')) - 3600*timezone[0]
		      end_time = time.mktime(time.strptime(str_end, '%m%d%Y %H:%M:%S')) - 3600*timezone[0]
#		      print numdays
		      value1 = datetime.datetime.fromtimestamp(start_time)
		      str_day = value1.strftime('%b')
                      str_day_array.append(str_day)
                      cur.execute("""SELECT ind, DT, Reading, M_Usage FROM Utils.scm_hist WHERE (((DT >= %s) and (DT < %s)) and ID=%s)""", (start_time, end_time, UtilsID))
                      res = cur.fetchall()
                      if len(res) > 0:
                           if (month):
			        rows1 = res[len(res)-1]
				rows2 = rows1
			 	row1[x] = rows1[2]
                                row2[x] = rows2[2]
			   else:
			        rows1 = res[len(res)-1]
                                rows2 = res[0]
                                row1[x] = rows1[2]
                                row2[x] = rows2[2]
                      else:
                           row1[x] = 0
                           row2[x] = 0

                      if ((row2[x] != 0) and  (row1[x] != 0)):
			  if (month):
			       u_diff[x] = row1[x]
			  else:
                      	       u_diff[x] = row1[x] - row2[x]
                      else:
                           u_diff[x] = 0

 		      if cur_month == 12:
                           cur_month = 1
                           cur_year = cur_year + 1
                      else:
                           cur_month = cur_month + 1
		 if (month):
		      for x in range(1, 12):
			   if u_diff[x-1] != 0:
			        u_diff1[x] =  (u_diff[x] - u_diff[x-1])
                           else:
				u_diff1[x] = 0
		      print u_diff1/100
		      cur.execute("""UPDATE Utils.utils_list SET CurDy = %s WHERE ID = %s""", (u_diff1[11], UtilsID))
                      cur.execute("""UPDATE Utils.utils_list SET LstDy = %s WHERE ID = %s""", (u_diff1[10], UtilsID))
		 else:
		      print u_diff/100
                 print str_day_array
                 plt.figure(figsize=(4,3))#
		 matplotlib.rcParams.update({'font.size': 8})
                 N = 12 #len(diff)
                 ind = np.arange(N)
                 width = 0.4
		 if UtilsName[0] == 'E':
                      rects1 = plt.bar(ind, u_diff/100, width, color='g', label='kWh')
                      legend = plt.legend(loc='upper left', shadow=True)
                      for rect in rects1:
                           height = rect.get_height()
			   if height > 0:
                                plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '$%.2f'%float(height*price),
                                ha='center', va='bottom')
                      x1,x2,y1,y2 = plt.axis()
                      plt.axis((x1-.5,x2,y1,y2+12))
                      plt.ylabel('kWh')
		      cur_time = datetime.datetime.fromtimestamp(time.time() + 3600*timezone[0])
                      str_day = cur_time.strftime('%m/%d/%Y %H:%M:%S')
                      plt.xlabel('Generated: '+ str_day)
                      plt.title(metername+': kWh Usage ($'+str(format((u_diff.sum()/100)*price, '.2f'))+')')
                      plt.xticks(ind+width/2,str_day_array)
                      plt.show()
                      plt.savefig("/var/www/months_"+str(UtilsName)+"_"+str(UtilsID)+".png")
		 elif UtilsName[0] == 'G':
		      if (month):
		           rects1 = plt.bar(ind, u_diff1/100, width, color='g', label='CCF')

		      else:
		           rects1 = plt.bar(ind, u_diff/100, width, color='g', label='CCF')
                      legend = plt.legend(loc='upper left', shadow=True)
                      for rect in rects1:
                           height = rect.get_height()
                           if height > 0:
                                plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '$%.2f'%float(height*price),
                                ha='center', va='bottom')
                      x1,x2,y1,y2 = plt.axis()
                      plt.axis((x1-.5,x2,y1,y2+12))
                      plt.ylabel('CCF')
                      cur_time = datetime.datetime.fromtimestamp(time.time() + 3600*timezone[0])
                      str_day = cur_time.strftime('%m/%d/%Y %H:%M:%S')
                      plt.xlabel('Generated: '+ str_day)
		      if (month):
			   plt.title(metername+': CCF Usage ($'+str(format((u_diff1.sum()/100)*price, '.2f'))+')')
		      else:
                           plt.title(metername+': CCF Usage ($'+str(format((u_diff.sum()/100)*price, '.2f'))+')')
                      plt.xticks(ind+width/2,str_day_array)
                      plt.show()
                      plt.savefig("/var/www/months_"+str(UtilsName)+"_"+str(UtilsID)+".png")

      db.commit()
      cur.close()
      db.close()
