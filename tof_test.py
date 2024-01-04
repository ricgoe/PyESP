import time
from machine import Pin
from machine import I2C
import tof as VL53L0X

#i2c = I2C(1)
#i2c = I2C(0, I2C.MASTER)
scl_pin = Pin(22, Pin.OUT)  # SCL pin
sda_pin = Pin(21, Pin.OUT)  # SDA pin
i2c = I2C(1, scl=scl_pin, sda=sda_pin)

#i2c.init(0,scl=scl_pin, sda=sda_pin, freq=100000)

#i2c.init(scl = scl_pin, sda = sda_pin)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)

i = 0
while i < 10:
# Start ranging
    tof.start()
    tof.read()
    print(tof.read())
    tof.stop()
    i += 1
