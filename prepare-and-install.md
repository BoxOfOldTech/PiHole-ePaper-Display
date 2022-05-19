The install
---------------
there are many ways to go from here, but this is what i did.

Insstall RaspberryPi Os Buster w/gui
- choose language, login,..
- set up ssh, i2c, spi, vnc, remote GPIO ..
- install Mu or/and thorny (just to be able to edit script on the devise)
- rightclick net icon in topline - network setting - wlan0 - choos an static ip - turn wifi off/on
- now go via vnc

(GPIO are normaly already installed!! but else: "sudo apt-get install rpi.gpio")

this process is snipped from "https://pimylifeup.com/raspberry-pi-low-voltage-warning/"
- edit: sudo nano /boot/config.txt
- add line in bottom: avoid_warnings=1
- save and exit
- remove bat monitor: sudo apt remove lxplug-ptbatt
- reboot 

this process is snipped from "https://pi-hole.net/" 
- install: curl -sSL https://install.pi-hole.net | bash

(it get some lang error wen doing via gui. but works)

this process is snipped from  "https://github.com/PiSupply/PaPiRus" 
- install: curl -sSL https://pisupp.ly/papiruscode | sudo bash

this process is snipped from https://github.com/Ewpratten/pihole-api 
- install: python3 -m pip install --no-cache-dir PiHole-api

getting the fontfile:
- install: wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/pihole/VCR_OSD_MONO_1.001.ttf
- alternative install: wget (https://github.com/3ndG4me/Font/blob/master/VCR_OSD_MONO_1.001.ttf)

getting the fontfile for bargraf:
- freemono fontlist: https://blogfonts.com/free-monospaced.font
- i just downloaded it and copy it to same directory as the OSD_MONO font

set up autostart script in gui:
tried many things but this looks like it works, just as expected.
- edit: sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
- add line, to run in terminal window in GUI: "@lxterminal -e /usr/bin/python3 /home/pi/pihole-display.py"
> or,
> add this line to run in background: "@/usr/bin/python3 /home/pi/pihole-displa2.py"
