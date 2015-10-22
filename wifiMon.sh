/bin/ping -q -c1 google.com > /dev/null
#echo "Got Here"
if [ $? -eq  0 ]
then
    echo "Network active"

else
  echo "Network down, fixing..."
#  ifdown --force wlan0
  /bin/kill -9 `pidof wpa_supplicant`
  /sbin/ifup --force wlan0
  /sbin/ip route add default via 192.168.1.1 dev wlan0
  sudo reboot
fi

