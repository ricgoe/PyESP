import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
from io import StringIO
import os
import pandas as pd

# Configuration
broker = "192.168.178.152"
port = 1883

def sender(**kwargs):
    # Create a client instance
    client = mqtt.Client()

    try:
        # Connect to the broker
        client.connect(broker, port)

        # Publish a message
        client.publish("calibration", json.dumps(kwargs).encode('utf-8'))


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect the client
        client.disconnect()
         
def listener():
    client = mqtt.Client()
    client.connect(broker, port)
    client.subscribe("calib_data")
    client.on_message = on_message
    client.loop_forever()


def on_message(client: mqtt.Client, userdata, msg):
    if msg.payload.decode('utf-8') == "stop":
        client.loop_stop()
        client.disconnect()
        return
    
    df = pd.read_csv(StringIO(msg.payload.decode('utf-8')))
    print(df)
    output_filename=f'calibration_pos_{str(df.iloc[-1,-3])}_rot_{str(df.iloc[-1,-2])}_mode_{str(df.iloc[-1,-1])}.csv'
    output_path = os.path.join(os.getcwd(), 'Calibration_files')
    output_filepath = os.path.join(output_path, output_filename)
    df.to_csv(output_filepath, mode='a', header=not os.path.exists(output_filepath), index=False)
    fig, ax = plt.subplots(figsize = (16, 8))
    ax.plot(df.columns[:-3], df.iloc[0, :-3])
    #ax.set_ylim(75, 200)
    ax.set_xticks([x for x in range(0,len(df.columns), 8)])
    plt.show()

    

if __name__ == '__main__':
    # sensor_rotation = 1 -> sensor is rotated vertically, sensor_rotation = 0 -> sensor is rotated horizontally
    sender(password="jimmy4", stop=False, position = 7, sensor_rotation = 0, mode = 'cube')
    listener()

    