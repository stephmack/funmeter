#!/bin/bash
if [ "$1" == "startamrscm" ]; then
    if pgrep rtlamr > /dev/null
    then
        echo "rtlamr_scm already running"
    else
	if [ -z "$2" ]
	then
	     /home/pi/bin/rtlamr -msgtype=scm & #-format=json -filterid=42470507,47703369,1481610912 -logfile=DataLog.json &
             echo "rtlamr_scm  started, No Utils Specified"
	else
	     /home/pi/bin/rtlamr -msgtype=scm -filterid="$2" &
             echo "rtlamr_scm  started, Utils $2 Specified"
	fi
    fi
fi

if [ "$1" == "startamridm" ]; then
    if pgrep rtlamr > /dev/null
    then
        echo "rtlamr_idm already running"
    else
        /home/pi/bin/rtlamr -msgtype=idm &
        echo "rtlamr_idm  started"
    fi
fi

if [ "$1" == "startamrr900" ]; then
    if pgrep rtlamr > /dev/null
    then
        echo "rtlamr_r900 already running"
    else
        /home/pi/bin/rtlamr -msgtype=r900 &
        echo "rtlamr_r900  started"
    fi
fi

if [ "$1" == "stopamr" ]; then
    if pgrep rtlamr
    then
        kill $(pgrep rtlamr) > /dev/null 2>&1
        echo "rtlamr stopped"
    else
        echo "rtlamr  not running"
    fi

    if pgrep rtlamr
    then
        kill $(pgrep rtl_tcp) > /dev/null 2>&1
        echo "rtl_tcp stopped"
    else
        echo "rtl_tcp  not running"
    fi
fi

if [ "$1" == "stoptcp" ]; then
    if pgrep rtl_tcp
    then
        kill $(pgrep rtl_tcp) > /dev/null 2>&1
        echo "rtl_tcp stopped"
    else
        echo "rtl_tcp  not running"
    fi
fi

if [ "$1" == "starttcp" ]; then
    if pgrep rtl_tcp > /dev/null
    then
        echo "rtl_tcp already running"
    else
        /usr/bin/rtl_tcp &
        echo "rtl_tcp  started"
    fi
fi
if [ "$1" == "tcpcheck" ]; then
    runstop=0
    if pgrep -f "python /home/pi/EnergyMon/py/console.py" > /dev/null; then
        echo "Conole running"
        #exit
    else
        echo "Console NOT running"
        runstop=1
    fi
    if pgrep rtl_tcp > /dev/null; then
        echo "trl_tcp running"
        #exit
    else
        echo "rtl_tcp NOT running"
        runstop=1
    fi
    if pgrep rtlamr > /dev/null; then
        echo "rtlamr running"
        #exit
    else
        echo "rtlamr NOT running"
        runstop=1
    fi
    echo $runstop
    if [ "$runstop" == "0" ]; then
        echo "No Action Required..."
    else
        echo "Console, rtlamr, or rtl_tcp  NOT running... Killing, Restarting All..."
        kill $(pgrep rtl_tcp) > /dev/null 2>&1
        kill $(pgrep rtlamr) > /dev/null 2>&1
        kill $(pgrep -f "python /home/pi/EnergyMon/py/console.py") > /dev/null 2>&1
        sleep 30
        sudo python /home/pi/EnergyMon/py/console.py &
    fi
fi
