import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import os

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
        client.publish("start", json.dumps(kwargs).encode('utf-8'))


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect the client
        client.disconnect()
         
def listener():
    client = mqtt.Client()
    client.connect(broker, port)
    client.subscribe("data")
    client.on_message = on_message
    client.loop_forever()


def on_message(client: mqtt.Client, userdata, msg):
    if msg.payload.decode('utf-8') == "stop":
        client.loop_stop()
        client.disconnect()
        return
    
    
    df = pd.read_csv(StringIO(msg.payload.decode('utf-8')))
    print(df)
    #df.to_csv("data_test_2.csv", index=False)
    output_filename=f'scans_angle_{str(df.iloc[-1,-1]).replace('.','_')}_pos_{str(df.iloc[-1,-3])}_rot_{str(df.iloc[-1,-2])}.csv'
    #output_path = os.path.join(os.getcwd(), 'Logs_Multi')
    output_path = os.path.join(os.getcwd(), 'Logs')
    output_filepath = os.path.join(output_path, output_filename)
    df.to_csv(output_filepath, mode='a', header=not os.path.exists(output_filepath), index=False)
    #df.to_csv('test.csv', index=False)
    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    #ax.plot(df.columns[:-1], df.iloc[0, :-1])
    # ax.plot(df.columns[:-1], df.iloc[0, :-1], 'o-', label='Messreihe 1') # Linie mit Punkten
    #ax.set_ylim(0, 250)
    #ax.set_xticks([x for x in range(0, len(df.columns), 8)])
    #ax.set_rmax(12) # Maximaler Radius
    # ax.set_rticks([4, 6, 8, 10]) # Radien-Markierungen
    # ax.set_rlabel_position(-22.5) # Position der Radien-Beschriftung
    # ax.grid(True)
    # ax.legend(loc='upper right') # Legende
    # plt.show()
    # fig, ax = plt.subplots(figsize = (16, 8))
    # ax.plot(df.columns[:-4], df.iloc[0, :-4])
    # #ax.set_ylim(75, 200)
    # ax.set_xticks([x for x in range(0,len(df.columns), 8)])
    # plt.show()
    

if __name__ == '__main__':
    # sensor_rotation = 1 -> sensor is rotated vertically, sensor_rotation = 0 -> sensor is rotated horizontally
    sender(password="jimmy4", angle=11.25, stop=False, runs=200, shape="prisma", mode = "angle", position = 4, sensor_rotation = 0)
    listener()

    