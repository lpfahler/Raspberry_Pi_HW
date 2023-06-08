# Program to use a DHT-11 temperature and humidity sensor with a Raspberry Pi
# and an LCD1602A display - show temp and humidity on display
# HW for McWhorter's Raspberry Pi Lesson 25(B) - two lessons are #25

# Loaded LCD1602.py file into program directory to use this display
# Display needs 5V to work properly
# Installed dht11 library using 'pip3 install dht11'
# Lori Pfahler
# May 2023

# load modules
from gpiozero import Button
from time import sleep
import dht11
import LCD1602

# intialize LCD, DHT-11, and button
LCD1602.init(0x27, 1)
myDHT11 = dht11.DHT11(pin=17)
myButton = Button(21)

# variable to switch scales from deg C(True) to deg F(False)
toggleScale = True

# get initial value for temperature
result = myDHT11.read()
while result.is_valid == False:
    result = myDHT11.read()
    sleep(2)

# function to run when button is released
def toggle_scale():
    global toggleScale
    toggleScale = not toggleScale
    
myButton.when_released = toggle_scale

try:
    while True:
        result = myDHT11.read()
        if result.is_valid():
            print('update to stats')
            # Column, Row numbering system - reverse of what you expect
            if toggleScale == True:
                LCD1602.write(0, 0, 'DHT11 T(C) ' + str(result.temperature))
            else:
                tempF = round((result.temperature * 1.8) + 32, 1)
                LCD1602.write(0, 0, 'DHT11 T(F) ' + str(tempF))
            LCD1602.write(6, 1, 'H(%) ' + str(result.humidity))
            sleep(2)
        

except KeyboardInterrupt:
    LCD1602.clear()