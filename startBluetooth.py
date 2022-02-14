import os
import glob
import time
import subprocess
import shlex
import base64

from time import sleep
from PIL import Image
from io import BytesIO

from bluetooth import *

try:
    import httplib
except:
    import http.client as httplib

from wifi import Cell, Scheme
wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "Raspy",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

def ssid_available():
    Cells = Cell.all('wlan0')
    wifi_info = 'Found ssid : \n'
    for current in range(len(Cells)):
        wifi_info +=  Cells[current].ssid + "\n"
    wifi_info+="!^"
    print wifi_info
    return wifi_info

def isWiFi():
	ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	try:
		output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
		return True
	except subprocess.CalledProcessError:
		return False

	
while True:          
	print "Waiting for connection on RFCOMM channel %d" % port
	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info
	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0: break
			if "listSSID" in data:
				print "received [%s]" % data
				client_sock.send(ssid_available())
			elif "checkConnection" in data:
				print "received [%s]" % data

				if isWiFi():
					conn = httplib.HTTPConnection("www.google.com", timeout=5)
					try:
						conn.request("HEAD", "/")
						client_sock.send("CONNECTION_AVAILABLE\i")
					except:
						client_sock.send("CONNECTION_NOT_AVAILABLE\i")
				else:
					client_sock.send("WIFI_NOT_AVAILABLE\i")
			else:
				client_sock.send("KNF!!!")
				print "Key not found"
		
	except IOError:
		pass

	except Exception as e:
		print(e)
		print "Exception"
		client_sock.close()
		server_sock.close()
		

	except KeyboardInterrupt:
		print "disconnected"
		client_sock.close()
		server_sock.close()
		print "all done"
		break