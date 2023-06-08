# Program to use a DHT-11 temperature and humidity sensor with a Raspberry Pi
# From McWhorter's Raspberry Pi Lesson #25
# Lori Pfahler
# Installed dht11 library using 'pip3 install dht11'
# May 2023

import RPi.GPIO as GPIO
import dht11
from time import sleep

GPIO.setmode(GPIO.BCM)
myDHT11 = dht11.DHT11(pin=17)

sleep(2)

# bad readings
nBad = 0
# total number of attempts at reading
nTotal = 0

try:
    while True:
        result=myDHT11.read()
        if result.is_valid():
            print('Temp is: ', result.temperature, ' degC, Humidity is: ', result.humidity, '%', sep = '')
        else:
            print("Bad Reading")
            nBad += 1
        nTotal += 1
        sleep(2)
        

except KeyboardInterrupt:
    print(f"DHT-11: Percent Invalid: {nBad/nTotal:>3.1%}, #bad: {nBad:>3}, total: {nTotal:>3}")
    GPIO.cleanup()