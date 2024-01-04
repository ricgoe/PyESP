# type: ignore
import utime
from umqtt.simple import MQTTClient
from sensor import Sensor
from stepper import Stepper
import json
import VL53L0X
from machine import Pin, I2C

# Configuration
SERVER = "10.42.0.1"
PORT = 1883
TOPIC = b"start"
with open("continue", "r") as f:
    should_stop_listening = f.read() == "0"
should_stop_listening = False # Debug
# my_sensor = Sensor(trigger_pin=12, echo_pin=33)

scl_pin = Pin(22, Pin.OUT)  # SCL pin
sda_pin = Pin(21, Pin.OUT)  # SDA pin
i2c = I2C(1, scl=scl_pin, sda=sda_pin)
vl_driver = VL53L0X.VL53L0X(i2c)
vl_driver.init(power2v8=False)

my_stepper = Stepper(19, 18, 5, 17)

FULL_ROTATION = int(4075.7728395061727 / 8)

# Callback function to handle messages
def on_message(topic, msg):
    global should_stop_listening
    print("Topic: %s, Message: %s" % (topic, msg))
    my_dick = json.loads(msg)
    
    if my_dick["password"] == "jimmy4":
        vl_driver.set_Vcsel_pulse_period(vl_driver.vcsel_period_type[0], 12)
        vl_driver.set_Vcsel_pulse_period(vl_driver.vcsel_period_type[1], 8)
        iterations = int(360/my_dick["angle"]) if my_dick["mode"]=="angle" else int(FULL_ROTATION/my_dick["angle"])
        factor = my_dick["angle"] if my_dick["mode"] == "angle" else int(FULL_ROTATION/360)
        data = ",".join([f"{(i)*factor}" for i in range(iterations)]) + ",shape\n"
        for _ in range(my_dick["runs"]):
            
            vl_driver.start()
            vl_driver.read()-36
            vl_driver.stop()
            
            for i in range(iterations):
                
                vl_driver.start()
                dist=vl_driver.read()-36
                vl_driver.stop()
                # print(vl_driver.read()-40) #DEBUG
                utime.sleep(0.02)
                my_stepper.angle(my_dick["angle"])
                utime.sleep(0.005)
                data += str(dist) + ','
                utime.sleep(1)
            
            data += my_dick["shape"]+'\n'
            utime.sleep(1)
    
    if my_dick["stop"]:
        should_stop_listening = True
        with open("continue", "w") as f:
            f.write("0")

    client = MQTTClient("ESP32DATA", SERVER, PORT)
    try:
        client.connect()
        client.publish(b"data", data)
        print(data)
    except Exception as e:
        print("Error1: %s" % e)
    finally:
        try:
            client.disconnect()
        except Exception as e:
            print("Error2: %s" % e)
    

def main():
    global should_stop_listening
    client = MQTTClient("ESP32", SERVER, port=PORT)
    client.set_callback(on_message)

    try:
        client.connect()
        print("Connected to %s:%s" % (SERVER, PORT))
        client.subscribe(TOPIC)
        print("Subscribed to %s" % TOPIC)

        while not should_stop_listening:
            # Check for new messages
            client.check_msg()
            utime.sleep(1)
    
    except Exception as e:
        print("Error: %s" % e)
    
    finally:
        try:
            client.disconnect()
        except Exception:
            pass

if __name__ == "__main__":
    main()
