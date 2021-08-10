# adafruit esp8266 feather, esp-12, esp8266 desk temperature device,
#
# peripherals; ds18b20 sensor on pin 5, 4k7 pull-up resistor,
#
# listens for UDP packets, and when a packet is received the payload
# is discarded, the temperature sensor is read, and the result
# returned to the remote host by UDP,
#
from machine import Pin, Timer
from network import WLAN, STA_IF, AP_IF
from time import sleep_ms
import socket
import onewire
import ds18x20

ESSID = 'essid'            # name of office wireless network
PASSPHRASE = 'passphrase'  # password for network
PORT = 7400                # port number

p0 = Pin(0, Pin.OUT)  # adafruit esp8266 feather, red led, inverted drive
p2 = Pin(2, Pin.OUT)  # esp-12 module, blue led, inverted drive

ap = WLAN(AP_IF)
ap.active(False)

sta = WLAN(STA_IF)
sta.active(True)
sta.connect(ESSID, PASSPHRASE)

while not sta.isconnected():
    print('.', end='')
    p2.off()
    sleep_ms(100)
    p2.on()
    sleep_ms(100)

ui = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ui.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ui.bind(('', PORT))

print()
print(sta.ifconfig()[0])  # display the IP address given by DHCP query

p2.off()

def led_off(t):
    p2.on()

def led_on(t):
    p2.off()
    t0.init(period=10, mode=Timer.ONE_SHOT, callback=led_off)

t0 = Timer(-1)
t1 = Timer(-1)
t1.init(period=100, mode=Timer.PERIODIC, callback=led_on)

ow = onewire.OneWire(Pin(5))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

addr = ''
for byte in roms[0]:
    addr += '%02X' % byte

while True:
    (pack, peer) = ui.recvfrom(128)

    p0.off()
    ds.convert_temp()
    sleep_ms(150)
    p0.on()
    sleep_ms(600)

    pack = '%s,%d' % (addr, int(ds.read_temp(roms[0])*10000))
    print(pack)
    _ = ui.sendto(pack, peer)
    Pin(2, Pin.OUT).on()
