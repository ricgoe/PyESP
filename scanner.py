from sensor import Sensor
from stepper import Stepper
import time

my_sensor = Sensor(trigger_pin=12, echo_pin=25)
my_stepper = Stepper(19, 18, 5, 17)
fr = Stepper.FULL_ROTATION


def _make_log(step_size:int, shape):
    with open(f"{shape}_step_{step_size}.csv", "x") as f:
        f.write(",".join([f"{i+1}" for i in range(int(fr/step_size))]))
        f.write(",shape"+"\n")
def log(shape, step_size):
    print(f"Shape: {shape}, Step size: {step_size}")
    try:
        _make_log(step_size, shape)
    except Exception as e:
        pass
    with open(f"{shape}_step_{step_size}.csv", "a") as f:
        for _ in range(int(fr/step_size)):
            my_stepper.step(step_size)
            dist = my_sensor.distance_mm()
            f.write(f"{dist},")
        f.write(shape+"\n")
    
def main(iterations, shape, step_size):    
    for i in range(iterations):
        log(shape, step_size)
        print(f"At {i+1} iterations")
        time.sleep(1)
        my_stepper.step(3)
        time.sleep(1)
        
main(15, "pyramid", 1)