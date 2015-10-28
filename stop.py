import os

os.system('sudo /etc/init.d/heartbeat.sh stop')
os.system('sudo /etc/init.d/console.sh stop')
os.system('sudo /etc/init.d/rtl_tcp stop')
os.system('sudo /etc/init.d/rtlamr stop')
