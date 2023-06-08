# Program to use a DHT-11 and DHT-22 temperature and humidity sensors
# on a Raspberry Pi using pigpio_dht library
# From McWhorter's Raspberry Pi Lesson #25
# Lori Pfahler
# May 2023

# Must start pigpio daemon to use the pigpio library
# In terminal, type:  'sudo pigpiod'

from pigpio_dht import DHT11, DHT22
from time import sleep

# initialize
myDHT11 = DHT11(17)
myDHT22 = DHT22(22)

sleep(2)

'''
results from .read() - in dictionary
DHT11 Results:
{'temp_c': 23, 'temp_f': 73.4, 'humidity': 40, 'valid': True}
DHT22 Results:
{'temp_c': 21.9, 'temp_f': 71.4, 'humidity': 41.4, 'valid': True}
'''

# bad readings
nBad_11 = 0
nBad_22 = 0
# total number of attempts at reading
nTotal = 0

try:
    while True:
        nTotal += 1
        DHT11Results = myDHT11.read(1)
        DHT22Results = myDHT22.read(1)
        if DHT11Results['valid'] == False:
            nBad_11 += 1
        if DHT22Results['valid'] == False:
            nBad_22 += 1    
    #    DHT11Results = myDHT11.sample(samples = 5)
    #    DHT22Results = myDHT22.sample(samples = 5)
        print('DHT11 Results:')
        print(DHT11Results)
        print('DHT22 Results:')
        print(DHT22Results)
        sleep(2)

except KeyboardInterrupt:
    print(f"DHT-11: Percent Invalid: {nBad_11/nTotal:>3.1%}, #bad: {nBad_11:>3}, total: {nTotal:>3}")
    print(f"DHT-22: Percent Invalid: {nBad_11/nTotal:>3.1%}, #bad: {nBad_11:>3}, total: {nTotal:>3}")
    