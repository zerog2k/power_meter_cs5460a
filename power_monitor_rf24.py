#!/usr/bin/env python

#  receive values from CS5460A power monitor via NRF24L01
#  may need to run as sudo
#  see https://github.com/zerog2k/power_meter_cs5460a for arduino transmitter code

import time as time
from RF24 import *
import RPi.GPIO as GPIO
import binascii
import struct
from datetime import datetime, date

MSGTYPES = [ "MSG_POWER_METER" ]

irq_gpio_pin = None

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/RPi/pyRF24/readme.md

# CE Pin, CSN Pin, SPI Speed

#RPi B+
# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
radio = RF24(RPI_BPLUS_GPIO_J8_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_1MHZ)

# Setup for connected IRQ pin, GPIO 24 on RPi B+; uncomment to activate
#irq_gpio_pin = RPI_BPLUS_GPIO_J8_18
#irq_gpio_pin = 24

pipes = [0x4A454E5300]

radio.begin()

radio.setChannel( 1 )
# set datarate  
radio.setDataRate( RF24_250KBPS )
#radio.setPALevel(RF24_PA_MAX)
radio.enableDynamicPayloads()

radio.printDetails()

radio.openReadingPipe(0, pipes[0])
radio.startListening()

dt = datetime

pipenum = -1

# forever loop
while True:
  try:
    have_data, pipenum = radio.available_pipe()
    if have_data:
        len = radio.getDynamicPayloadSize()
        if len > 0:
            msgtype = radio.read(1);
        receive_payload = radio.read(len)

        if msgtype[0] == MSGTYPES.index("MSG_POWER_METER"):
            (voltage, current, true_power, power_factor) = struct.unpack_from("ffff", receive_payload, 1)
            print "%s pipe: %d, msgtype: %s, voltage: %0.1f, current: %0.2f, true_power: %0.1f, PF: %0.2f" \
                % (dt.now(), pipenum, MSGTYPES[msgtype[0]], voltage, current, true_power, power_factor)
        else:
            print "%s got: pipe=%d size=%s raw=%s" % (dt.now(), pipenum, len, binascii.hexlify(receive_payload))
    time.sleep(1)
  except Exception as e:
     print e.strerror


