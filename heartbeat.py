import os
import time
import dbfunc
import radio_rec
#time1 = time.time()
time1_int = 720  

radio_rec.radio_check()

while(1):
#     if (time.time() - time1 >= time1_int):
      try: 
           print 'Running Hearbeat'    
           radio_rec.radio_check()
      except:
	   print 'Error HeartBeat...'
#          time1 = time.time()
      time.sleep(time1_int)
