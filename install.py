import os
import shutil
import MySQLdb
import warnings

warnings.filterwarnings("error")
os.system('sudo python filedwnld.py')
os.system('sudo python compile.py')
os.system('sudo python routine.py')

#clean Up
os.system('sudo rm -rf /home/pi/EnergyMon/py/funmeter')
os.system('sudo reboot')
