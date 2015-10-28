#!/usr/bin/env python
import os
import time
import dbfunc
import subprocess
import urllib2

#os.system('sudo rm /home/pi/heartbeat.log')
i = 0
#time1 = time.time()
time1_int = 720  

#radio_rec.radio_check()
def radio_check():
#if (1):
        try:
                response=urllib2.urlopen('http://www.google.com',timeout=1)
                print 'Network Connection Active...'
        except:
                print 'No Network Connection... Rebooting...'
                os.system('sudo reboot')

        #proc = subprocess.Popen(["sudo /etc/init.d/heartbeat.sh status"], stdout=subprocess.PIPE, shell=True)
        #(outhb, err) = proc.communicate()
        proc = subprocess.Popen(["sudo /etc/init.d/rtl_tcp status"], stdout=subprocess.PIPE, shell=True)
        (outtcp, err) = proc.communicate()
        proc = subprocess.Popen(["sudo /etc/init.d/rtlamr status"], stdout=subprocess.PIPE, shell=True)
        (outamr, err) = proc.communicate()
        proc = subprocess.Popen(["sudo /etc/init.d/console.sh status"], stdout=subprocess.PIPE, shell=True)
        (outcs, err) = proc.communicate()
        print outtcp.find('failed'), outamr.find('failed'), outcs.find('failed')
        if ((outcs.find('failed') == -1) and (outtcp.find('failed') == -1) and (outamr.find('failed') == -1)):
                print 'All services running...'
        else:
                print 'One of the services is not running, restarting all...'
                os.system('sudo /etc/init.d/rtl_tcp stop')
                os.system('sudo /etc/init.d/rtlamr stop')
                os.system('sudo /etc/init.d/console.sh stop')
                time.sleep(5)
                os.system('sudo /etc/init.d/rtl_tcp start')
                time.sleep(3)
                UtilsStr = dbfunc.Utils_List()
                os.system('sudo /etc/init.d/rtlamr start '+ UtilsStr)
                time.sleep(2)
                os.system('sudo /etc/init.d/console.sh start')



while(1):
      if i == 0:
	   print 'Starting heartbeat.py'
           radio_check()
   	   i = 1
      else:
           try: 
                print 'Running Hearbeat'    
                radio_check()
           except:
	        print 'Error HeartBeat...'
      time.sleep(time1_int)
