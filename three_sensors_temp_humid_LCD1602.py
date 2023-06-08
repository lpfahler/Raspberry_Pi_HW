# Program to use a DHT-11. DHT-22 and BME680 sensors 
# to measure temperature and humidity  with a Raspberry Pi
# Show results an LCD1602A display
# Use one button to cycle from deg C to deg F
# Use a second button to switch between sensors, DHT-11, DHT-22 and BME680
# HW for McWhorter's Raspberry Pi Lesson 25(B) - two lessons are #25

# Loaded LCD1602.py file into program directory to use this display
# Display needs 5V to work properly
# Installed dht11 library using 'pip3 install dht11'
# Lori Pfahler
# May 2023

# load modules
from gpiozero import Button
from time import sleep
from pigpio_dht import DHT11, DHT22
import LCD1602
import bme680

# intialize LCD, DHT-11, DHT-22 and buttons
LCD1602.init(0x27, 1)
myDHT11 = DHT11(17)
myDHT22 = DHT22(22)
# red button
tempButton = Button(21)
# blue button
sensorButton = Button(20)
# setup BME680 sensor
bmeSensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
bmeSensor.set_humidity_oversample(bme680.OS_2X)
bmeSensor.set_pressure_oversample(bme680.OS_4X)
bmeSensor.set_temperature_oversample(bme680.OS_8X)
bmeSensor.set_filter(bme680.FILTER_SIZE_3)

# function to run when tempButton is released
def toggle_scale():
    global toggleScale
    toggleScale = not toggleScale

# function to run when sensorButton is released
def switch_sensor():
    global switchSensor
    if switchSensor == 1:
        switchSensor = 2
    elif switchSensor == 2:
        switchSensor = 3
    else:
        switchSensor = 1

# variable to switch scales from deg C(True) to deg F(False)
toggleScale = True
# variable to switch sensors 1 = DHT-11, 2 = DHT-22, 3 = BME680
switchSensor = 3

tempButton.when_released = toggle_scale
sensorButton.when_released = switch_sensor

try:
    while True:    
        if switchSensor == 1:
            DHT11Results = myDHT11.read(1)
            if DHT11Results['valid']:
                LCD1602.clear()
                print('DHT-11: update to stats')
                # Column, Row numbering system - reverse of what you expect
                if toggleScale == True:
                    LCD1602.write(0, 0, 'DHT11 T(C) ' + str(DHT11Results['temp_c']))
                else:
                    LCD1602.write(0, 0, 'DHT11 T(F) ' + str(DHT11Results['temp_f']))
                LCD1602.write(6, 1, 'H(%) ' + str(DHT11Results['humidity']))
                sleep(1)
        if switchSensor == 2:
            DHT22Results = myDHT22.read(1)
            if DHT22Results['valid']:
                LCD1602.clear()
                print('DHT-22: update to stats')
                # Column, Row numbering system - reverse of what you expect
                if toggleScale == True:
                    LCD1602.write(0, 0, 'DHT22 T(C) ' + str(DHT22Results['temp_c']))
                else:
                    LCD1602.write(0, 0, 'DHT22 T(F) ' + str(DHT22Results['temp_f']))
                LCD1602.write(6, 1, 'H(%) ' + str(DHT22Results['humidity']))
                sleep(1)            
        if switchSensor == 3:
            bmeSensor.get_sensor_data()            
            if bmeSensor.get_sensor_data():
                LCD1602.clear()
                print('BME680: update to stats')
                # Column, Row numbering system - reverse of what you expect
                if toggleScale == True:
                    tempC = round(bmeSensor.data.temperature, 1)
                    LCD1602.write(0, 0, 'BME680 T(C) ' + str(tempC))
                else:
                    tempF = round((bmeSensor.data.temperature * 1.8) + 32, 1)
                    LCD1602.write(0, 0, 'BME680 T(F) ' + str(tempF))
                humid = round(bmeSensor.data.humidity, 1)
                LCD1602.write(7, 1, 'H(%) ' + str(humid))            
                sleep(1)
except KeyboardInterrupt:
    LCD1602.clear()
