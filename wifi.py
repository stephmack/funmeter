import os

def update_wpa_supplicant(ssid,passwd):
        ssid_val = ssid
        pass_val = passwd

        #Write SSID and PSK to wpa_supplicant.conf
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'rt') as f:
                s = f.read()
        #file1 = open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
        file = open('/home/pi/rpi_garage_smartthings/WiFi_parms.cfg','w')
        file.write(s)
        file.write('\n\nnetwork={\n        ssid="')
        file.write(ssid_val)
        file.write('"\n        psk="')
        file.write(pass_val)
        file.write('"\n')
        file.write('        key_mgmt=WPA-PSK')
        file.write('\n}')

        file.close()
        os.system('sudo mv /home/pi/rpi_garage_smartthings/WiFi_parms.cfg /etc/wpa_supplicant/wpa_supplicant.conf')

