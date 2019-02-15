install python package:
>> pip install smbus2

switch i2c to Repeated start mode: 
>> sudo sh -c '/bin/echo Y > /sys/module/i2c_bcm2708/parameters/combined'

