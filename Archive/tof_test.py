import time
from machine import Pin
from machine import I2C
import VL53L0X

#i2c = I2C(1)
#i2c = I2C(0, I2C.MASTER)
scl_pin = Pin(22, Pin.OUT)  # SCL pin
sda_pin = Pin(21, Pin.OUT)  # SDA pin
i2c = I2C(1, scl=scl_pin, sda=sda_pin)

#i2c.init(0,scl=scl_pin, sda=sda_pin, freq=100000)

#i2c.init(scl = scl_pin, sda = sda_pin)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

tof.init(power2v8=False)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

with open("offset.csv", "w") as f:
    # write number 1-25 in f seperated with ,
    for i in range(1000):
    # Start ranging
        tof.start()
        # print(tof.read())
        # log tof.read() in f
        f.write(str(i) + "," + str(tof.read()) + "\n")
        tof.stop()
