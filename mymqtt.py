# type: ignore
import utime
from umqtt.simple import MQTTClient
from sensor import Sensor
from stepper import Stepper
import json

# Configuration
SERVER = "10.42.0.1"
PORT = 1883
TOPIC = b"start"
with open("continue", "r") as f:
    should_stop_listening = f.read() == "0"
should_stop_listening = False # Debug
my_sensor = Sensor(trigger_pin=32, echo_pin=33)
my_stepper = Stepper(19, 18, 5, 17)

FULL_ROTATION = Stepper.FULL_ROTATION

def publish(datastr):
    client = MQTTClient("ESP32DATA", SERVER, PORT)
    try:
        client.connect()
        client.publish(b"data", datastr)
        print(datastr)
    except Exception as e:
        print("Error1: %s" % e)
    finally:
        try:
            client.disconnect()
        except Exception as e:
            print("Error2: %s" % e)

# Callback function to handle messages
def on_message(topic, msg):
    global should_stop_listening
    print("Topic: %s, Message: %s" % (topic, msg))
    my_dick = json.loads(msg)
    
    if my_dick['scan_mode'] == 'multi':
        publish('multiscanner')
    if my_dick["password"] != "jimmy4":
        return
    iterations = int(360/my_dick["angle"]) if my_dick["mode"]=="angle" else int(FULL_ROTATION/my_dick["angle"])
    #iterations = rotation_steps
    factor = my_dick["angle"] if my_dick["mode"] == "angle" else int(FULL_ROTATION/360)
    data = ",".join([f"{(i)*factor}" for i in range(iterations)]) + ",shape,position,sensor_rotation,angle\n"
    for i in range(my_dick["runs"]):
        for j in range(iterations):
            my_stepper.angle(my_dick["angle"]) if my_dick['mode'] == 'angle' else my_stepper.step(my_dick["angle"])
            utime.sleep(0.1)
            dist = my_sensor.distance_mm()
            data += str(dist) + ','
        data += my_dick["shape"] + ','+ str(my_dick["position"]) + ',' + str(my_dick["sensor_rotation"]) + ',' + str(my_dick["angle"]) + '\n'
        my_stepper.angle(2.8125) if my_dick['shape'] != 'cylinder' else None
        if i%10 == 0 and i != 0: 
            publish(data)
            data = ""

    if my_dick["stop"]:
        should_stop_listening = True
        with open("continue", "w") as f:
            f.write("0")
    if not data: 
        publish(data)
    publish("stop")
    

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
