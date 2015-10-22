import time
import os

def start_radio(UtilsStr):
	os.system('sudo bash /home/pi/EnergyMon/sh/startstoprtl.sh starttcp')
	time.sleep(3)
	os.system('sudo bash /home/pi/EnergyMon/sh/startstoprtl.sh startamrscm '+ UtilsStr)

def stop_radio():
	#amr_proc = os.system('pgrep rtl_amr')
	#print amr_proc
	os.system('sudo bash /home/pi/EnergyMon/sh/startstoprtl.sh stopamr')
        time.sleep(3)
        os.system('sudo bash /home/pi/EnergyMon/sh/startstoprtl.sh stoptcp')

def radio_check():
	os.system('sudo bash /home/pi/EnergyMon/sh/startstoprtl.sh tcpcheck ')
        os.system("sudo bash /home/pi/EnergyMon/sh/wifiMon.sh")
