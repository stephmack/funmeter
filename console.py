#!/usr/bin/env python
import time 
import math 
import numpy as np 
import serial 
import os
import MySQLdb
import dbfunc
#import radio_rec
import plotfunc

#Time Stuff
time1 = time.time()
time1_int =  300  
time2 = time1
time2_int = 5
time3_int = 180#3600
time3 = time1
case = 0
#Read Utils
#UtilsStr = dbfunc.Utils_List()
#Start rtl_tcp and rtlamr
#radio_rec.start_radio(UtilsStr)
plotfunc.plot_seven()
plotfunc.plot_hour()
plotfunc.plot_day()
plotfunc.plot_month()
while(1):
     if (time.time() - time1 >= time1_int):
          try:
	       dbfunc.Utils_decimate()
	       #UtilsStr = dbfunc.Utils_List()
          except:
               print 'Error in Main Function...'
	  time1 = time.time()

     if (time.time() - time3 >= time3_int):
          try:
	       if case == 0:
                     plotfunc.plot_seven()
		     case = 1
	       elif case == 1:	
	             plotfunc.plot_hour()
		     case = 2
	       elif case == 2:
               	     plotfunc.plot_day()
		     case = 3
	       elif case == 3:
               	     plotfunc.plot_month()
		     case = 0
          except:
               print 'Error Plotting...'

          time3 = time.time()
     time.sleep(time2_int)
     try:
          dbfunc.ctrl()
     except:
          print 'Error in ctrl function...'
