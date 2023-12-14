from sensor import Sensor
from stepper import Stepper
import time


my_sensor = Sensor(trigger_pin=12, echo_pin=25)
my_stepper = Stepper(19, 18, 5, 17)

for i in range(20):#
    print(my_sensor.distance_cm())
    my_stepper.step(10)


