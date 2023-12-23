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
my_sensor = Sensor(trigger_pin=12, echo_pin=33)
my_stepper = Stepper(19, 18, 5, 17)

# Callback function to handle messages
def on_message(topic, msg):
    global should_stop_listening
    print("Topic: %s, Message: %s" % (topic, msg))
    my_dick = json.loads(msg)
    
    if my_dick["password"] == "jimmy4":
        data = ",".join([f"{i+1}" for i in range(int(360/my_dick["angle"]))]) + ",shape\n"
        for _ in range(my_dick["runs"]):
            for i in range(int(360/my_dick["angle"])):
                my_stepper.angle(my_dick["angle"])
                utime.sleep(0.02)
                dist = my_sensor.distance_mm()
                utime.sleep(0.005)
                data += str(dist) + ','
                utime.sleep(0.005)
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
