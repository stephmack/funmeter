import os
import shutil
import MySQLdb
import warnings

warnings.filterwarnings("error")
##Compile rtl_tcp
os.chdir('/home/pi/EnergyMon/py/rtl-sdr/build')
os.system('cmake ../ cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DINSTALL_UDEV_RULES=ON')
os.system('make')
os.system('sudo make install')
os.system('sudo ldconfig')
os.chdir('/home/pi/EnergyMon/py')
##Compile rtlamr
os.chdir('/home/pi/src/github.com/bemasher/rtlamr')
os.system('ls')
os.system('sudo bash /home/pi/EnergyMon/sh/go_install.sh')
os.chdir('/home/pi/EnergyMon/py')

#Compile pi_garage_smartthings
os.chdir('/home/pi/pi_garage_smartthings')
os.system('sudo bash install.sh')
os.chdir('/home/pi/EnergyMon/py')