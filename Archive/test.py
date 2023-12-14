from machine import Pin
from time import sleep

light = Pin(1,Pin.OUT)
for i in range(10):
    light.on()
    sleep(0.5)
    light.off()
    sleep(0.5)