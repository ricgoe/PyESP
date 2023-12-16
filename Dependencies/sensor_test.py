from sensor import Sensor
from stepper import Stepper
from umqtt.simple import MQTTClient
import time

SERVER = '192.168.178.148'
CLIENT_ID = 'ESP_32_Dist'
TOPIC = b'dist_object'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

my_sensor = Sensor(trigger_pin=12, echo_pin=25)
my_stepper = Stepper(19, 18, 5, 17)

for i in range(50000):#
    dist = my_sensor.distance_cm()
    my_stepper.step(10)
    time.sleep(2)
    msg = (b'{0:3.1f}'.__format__(dist))
    client.publish(TOPIC, msg)
    print(msg)


