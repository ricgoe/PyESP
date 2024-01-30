from umqtt.simple import MQTTClient
import utime
from sensor import Sensor
from stepper import Stepper
import json

#calibration
SERVER = "10.42.0.1"
PORT = 1883
TOPIC = b"calibration"
should_stop_listening = False
my_sensor = Sensor(trigger_pin=32, echo_pin=33)
my_stepper = Stepper(19, 18, 5, 17)

FULL_ROTATION = Stepper.FULL_ROTATION
d_plate = 8 #mm

def publish_calib(datastr):
    client = MQTTClient("ESP32DATA", SERVER, PORT)
    try:
        client.connect()
        client.publish(b"calib_data", datastr)
        print(datastr)
    except Exception as e:
        print("Error1: %s" % e)
    finally:
        try:
            client.disconnect()
        except Exception as e:
            print("Error2: %s" % e)


def calibrate(topic, msg):
    global should_stop_listening
    print("Topic: %s, Message: %s" % (topic, msg))
    my_dick = json.loads(msg)
    
    data = ",".join([f"{(i)*2.8125}" for i in range(128)]) + ",position,sensor_rotation,mode\n"
    for i in range(128):

        utime.sleep(0.1)
        dist = my_sensor.distance_mm() if my_dick['mode'] == 'back' else my_sensor.distance_mm() + d_plate/2
        data += str(dist) + ','
    data += str(my_dick["position"]) + ',' + str(my_dick["sensor_rotation"]) + ',' + my_dick["mode"]

    if my_dick["stop"]:
        should_stop_listening = True
    
    publish_calib(data) 
    publish_calib('stop')
    
    
def main():
    client = MQTTClient("ESP32", SERVER, port=PORT)
    client.set_callback(calibrate)
    
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

if __name__ == '__main__':
    main()