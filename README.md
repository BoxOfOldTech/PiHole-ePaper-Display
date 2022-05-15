# PiHole-ePaper-Display

Hi there, This is a Pihole with an e-paper status display.
It is a raspberry pi, running a program, acting as an ad-blocker with a display.

It could run without a display but..
it is neat to see the statistics of the pi hole itself in an easy way. to check how effective it is.
And .. Well, I love to make small electronic projects and code. as one of my many hobbies.

For the build I settled for a Raspberry pi 3B - which I already had.
The display is a  PaPiRus HAT, from “Pi Supply”
And they even have a PaPiRus Enclosure to put it all in.
the perfect parts to my project.

What is PaPiRus?
The PaPiRus was originally launched on Kickstarter, and is now available to purchase on various online stores. 
The one I got has the largest e-paper screen and 4 tactile buttons on the top. The case has cutouts for the buttons and 4 small plastic things to put in the holes. All in all, a complete assembly.
https://uk.pi-supply.com/products/papirus-epaper-eink-screen-hat-for-raspberry-pi

######
The install:

insstall Raspbery py os Buster w/gui
 choose lan, login,..
	set up ssh, i2c, spi, vnc, remote GPIO ..
	install Mu, thorny
	rightclick net icon in topline - network setting - wlan0 - choos an static ip - turn wifi off/on
	now go via vnc

from "https://pimylifeup.com/raspberry-pi-low-voltage-warning/"
 - edit: sudo nano /boot/config.txt
 - add line in bottom: avoid_warnings=1
 - save and exit
 - remove bat monitor: sudo apt remove lxplug-ptbatt
 - reboot 

from "https://pi-hole.net/" install ->
curl -sSL https://install.pi-hole.net | bash
 - it get some lang error wen doing via gui. but works

from "https://github.com/PiSupply/PaPiRus" install ->
- curl -sSL https://pisupp.ly/papiruscode | sudo bash

from https://github.com/Ewpratten/pihole-api install ->
python3 -m pip install --no-cache-dir PiHole-api


fontfile:
wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/pihole/VCR_OSD_MONO_1.001.ttf
(https://github.com/3ndG4me/Font/blob/master/VCR_OSD_MONO_1.001.ttf)


(GPIO are normaly already installed!! : "sudo apt-get install rpi.gpio")


freemono fontlist: https://blogfonts.com/free-monospaced.font
- uset for bar graf


autostart script in gui:
tryed many things but this liks like it works.

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
add "@/usr/bin/python3 /home/pi/pihole-display2.py"
og to run in terminal window add "@lxterminal -e /usr/bin/python3 /home/pi/pihole-display2.py"

