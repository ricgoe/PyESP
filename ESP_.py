from sensor import Sensor
from stepper import Stepper
import time
from defaults import SHAPE, STEP_SIZE

my_sensor = Sensor(trigger_pin=12, echo_pin=25)
my_stepper = Stepper(19, 18, 5, 17)
valid_shapes = ["cube", "cylinder", "pyramid", "cone"]


def _make_log(step_size:int):
    with open(f"test_log_step_{step_size}.csv", "x") as f:
        f.write(",".join([f"{i+1}" for i in range(int(360/step_size))]))
        f.write(",shape"+"\n")
def main():
    shape = 'triangle'
    step_size = STEP_SIZE
    print(f"Shape: {shape}, Step size: {step_size}")
    try:
        _make_log(step_size)
    except Exception as e:
        print(e)
    with open(f"test_log_step_{step_size}.csv", "a") as f:
        for _ in range(int(360/step_size)):
            my_stepper.angle(step_size)
            dist = my_sensor.distance_mm()
            f.write(f"{dist},")
        f.write(shape+"\n")
    
for _ in range(50):
    main()
    time.sleep(4.5)