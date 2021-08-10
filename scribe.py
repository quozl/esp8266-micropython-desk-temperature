#!/usr/bin/python3
#
# logging script for desk temperature device
#
# every minute on the minute sends a UDP packet to the device, and
# when a reply is received prints the data and writes it to a file.
#
import socket
import time

IP = '10.0.0.1'  # address given to adafruit esp8266 feather by DHCP
PORT = 7400

files = {}
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.settimeout(0.1)

while True:
    time.sleep(60 - (time.time() % 60))
    socket.sendto(b'hello', (IP, PORT))
    try:
        (data, peer) = socket.recvfrom(128)
    except KeyboardInterrupt:
        print
        exit(1)
    except:
        print("error")
        continue
    ether, temp = data.decode().split(',')
    if ether not in files:
        files[ether] = open('%s.log' % ether, 'a', 1)
    try:
        print(ether, '%.3f\t%.4f' % (time.time(), float(temp)/10000.))
        print('%.3f\t%.4f' % (time.time(), float(temp)/10000.), file=files[ether])
    except:
        pass
