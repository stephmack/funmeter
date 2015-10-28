import os
import shutil
import MySQLdb
import warnings

warnings.filterwarnings("error")
os.system('sudo python /home/pi/EnergyMon/py/filedwnld.py')
os.system('sudo python /home/pi/EnergyMon/py/compile.py')
os.system('sudo python /home/pi/EnergyMon/py/routine.py')

#clean Up
os.system('sudo rm -rf /home/pi/EnergyMon/py/funmeter')
os.system('sudo reboot')
