# coding=utf-8
# Python program for showing Pihole stats on a PaPiRus HAT for Raspberry pi
#
# Date : 8. Apr. 2022, By Tech-Neek
# todo: automatic ip assigment, not done yet

#import libs
from papirus import PapirusTextPos
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time
import pihole as ph
import RPi.GPIO as GPIO
from datetime import datetime
from subprocess import Popen, PIPE

#Constant
font = "VCR_OSD_MONO_1.001.ttf"
font2="/usr/share/fonts/truetype/freefont/FreeMono.ttf" #for bargraf
text = PapirusTextPos(False,0)
pihole = ph.PiHole("192.168.1.19") # just a default IP

#Variable
global menu
global redraw_screen
global interface
global ip_address
menu=1
redraw_screen=1
global prc_max
prc_max = 0
global network_ping_ok
network_ping_ok = 0
global err_count
err_count = 0

#setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.setup(21, GPIO.IN)

##############################################
# functions
def check_connect(): #ping req.
    req = Request("http://www.google.com/")
    try: response = urlopen(req)
    except HTTPError as e:
        text.UpdateText("net_connect", "\u22a0")
        text.WriteAll(partialUpdate=1)
        print('- No conncection: Error code: ', e.code)
        return 0
    except URLError as e:
        text.UpdateText("net_connect", "\u22a0")
        text.WriteAll(partialUpdate=1)
        print('- No connection: Reason: ', e.reason)
        return 0
    else:
        text.UpdateText("net_connect", "\u221a")
        text.WriteAll(partialUpdate=1)
        print('- Networt connected, ping ok!')
        return 1

# looking for an active Ethernet or WiFi device
def find_interface():
    dev_name = "-"
    find_device = "ip addr show"
    p = Popen(find_device, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    interface_parse=output.decode('ascii')
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

# find an active IP on the first LIVE network device
def parse_ip():
    ip = "-"
    find_ip = "ip addr show %s" % interface
    p = Popen(find_ip, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    ip_parse=output.decode('ascii')
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

def pistat_updater():
    global interface
    global ip_address
    global network_ping_ok
    global err_count
    
    now = datetime.now()
    current_time = now.strftime("%-d/%-m %H:%M")
    print("*** UPDATE STAT ***")
    print("# time:", current_time)
    interface = find_interface()
    ip_address = parse_ip()
    print ("- Interface:", interface)
    print ("- IP adress: ", ip_address)
    network_ping_ok = check_connect()
    
    if (network_ping_ok == 1):
        print("> Updating pihole stats..")
        try: pihole.refresh()
        except OSError as e:
            print ("- Network Error: ", e)
            err_count = err_count + 1
            time.sleep(1)
        else:
            print ("- Update Success")
    else: err_count = err_count + 1
    print("# Uptime network error count: ",err_count)

def my_callback(channel):
    global menu
    global redraw_screen
    #print(channel)
    if(channel == 16):
        menu = 4
        redraw_screen = 1

    elif(channel == 21):
        menu = 1
        redraw_screen = 1
    #print(menu)

##############################################
def splash():
    text.Clear()
    text.AddText("PiHole Stats", 25, 30, size=30, fontPath=font )
    text.AddText("By: Tech-Neek 2022", 26, 70, size=18, fontPath=font )
    text.WriteAll()

def menu1_update(_partial_update):
    global prc_max
    now = datetime.now()
    current_time = now.strftime("%-d/%-m %H:%M")
    
    pistat_updater() # updating pihole stats
    text.UpdateText("ip_num",ip_address, fontPath=font)
    text.UpdateText("status",pihole.status, fontPath=font)
    text.UpdateText("q_num",pihole.queries, fontPath=font )
    text.UpdateText("b_num",pihole.blocked, fontPath=font )
    text.UpdateText("bp_num",pihole.ads_percentage, fontPath=font )
    text.UpdateText("time",current_time, fontPath=font )   
    ## make bargraf    
    bar = ""
    i = 0
    prc=int(float(pihole.ads_percentage)*20/100)
    if (prc > prc_max):prc_max = prc
    print ("- Block prc.:", prc, " Block prc.max:", prc_max)
    while (i <  prc):
        bar = bar + "\u2588" #bar
        i = i + 1
    if (i < prc_max):
            while (i < prc_max):
                bar = bar + "\u2591" 
                i = i + 1
    while (i < 20):
        bar = bar + "|" #outline
        i = i + 1
    text.UpdateText("bp_bar",bar, fontPath=font2 )
    print (bar)
    
    # update all screen
    text.WriteAll(partialUpdate=_partial_update)

def menu1_draw():
    text.Clear()
    text.AddText("PiHole DNS", 10, 10, Id="title", fontPath=font )
    text.AddText("check..", 170, 10, Id="status", fontPath=font )
    text.AddText("--------------------", 10, 25, Id="seperator", fontPath=font )
    text.AddText("IP:", 10, 40, Id="ip_text", fontPath=font )
    text.AddText(" ", 50, 40, Id="ip_num", fontPath=font )
    text.AddText(" ", 220, 40, Id="net_connect", invert=False, fontPath=font )
    text.AddText("Total Queries:", 10, 60, Id="q_text", fontPath=font )
    text.AddText(" ", 180, 60, Id="q_num", fontPath=font )
    text.AddText("Total Blocked:", 10, 80, Id="b_text", fontPath=font )
    text.AddText(" ", 180, 80, Id="b_num", fontPath=font )
    text.AddText("Blocked %:", 10, 100, Id="bp_text", fontPath=font )
    text.AddText(" ", 180, 100, Id="bp_num", fontPath=font )
    text.AddText(" ", 10, 125, Id="bp_bar", fontPath=font )
    text.AddText("Last update:", 10, 150, size=16, Id="time_text", fontPath=font )
    text.AddText(" ", 120, 150, size=16, Id="time", fontPath=font )
    text.WriteAll()
  
##############################################
#GPIO start event detect
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(21, GPIO.FALLING, callback=my_callback, bouncetime=300)

# prepair text to the screen
print ("## PiHole Stats, By: Tech-Neek 2022 ##")
splash()
print ("..Starting")
x=0
counter = 0
while 1:
    ## go menu 1
    if (menu ==1): # menu 1
        if (redraw_screen == 1):
            menu1_draw()
            redraw_screen = 0
            counter = 0
            menu1_update(True)#True for partial update
    
    ## go menu 4, quit
    if (menu ==4):# menu 4 - exit
        splash()
        quit()
    
    ## go idle count and auto update
    if (counter > 60*10): # auto update 10min delay
        if (menu > 1):
            menu = 1
            menu1_draw()
            redraw_screen = 0
        menu1_update(True)
        counter = 0        
    else:
        time.sleep(1)
        counter =  counter + 1
        
