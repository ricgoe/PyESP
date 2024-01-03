import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

# Configuration
broker = "10.42.0.1"
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
    df = pd.read_csv(StringIO(msg.payload.decode('utf-8')))
    print(df)
    df.to_csv("data_test.csv", index=False)
    fig, ax = plt.subplots(figsize = (16, 8))
    ax.plot(df.columns[:-1], df.iloc[0, :-1])
    ax.set_ylim(0, 250)
    ax.set_xticks([x for x in range(0,len(df.columns), 8)])
    plt.show()
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    sender(password="jimmy4", angle=2, stop=False, runs=1, shape="triangle")
    listener()
    
    
    