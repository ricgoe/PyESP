import stepper
from machine import Pin

stepper_motor = stepper.Stepper(Pin(19, Pin.OUT), Pin(18, Pin.OUT), Pin(5, Pin.OUT), Pin(17, Pin.OUT))

stepper_motor.step(100)