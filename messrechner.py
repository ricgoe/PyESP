from email.mime import image
import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import os
import numpy as np
from scipy.signal import medfilt
from scipy.fft import rfft, irfft, rfftfreq
from keras.models import load_model

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
    df = df.iloc[:,:-4]
    #print(df)
    output_filename=f'scans_angle_demo.csv'
    
    #output_path = os.path.join(os.getcwd(), 'Logs_Multi')
    output_path = os.path.join(os.getcwd(), 'DEMO')
    output_filepath = os.path.join(output_path, output_filename)
    df.to_csv(output_filepath, mode='a', header=not os.path.exists(output_filepath), index=False)
    
    median_window_size = 11
    values_df = df
    
    data_filtered_df = pd.DataFrame()
  
    for i in range(len(df)):
        data_filtered = medfilt(values_df.iloc[i], kernel_size=median_window_size)
        data_filtered_fft_int = fft_filter(data_filtered)
        data_filtered_df= pd.concat([data_filtered_df, pd.DataFrame(data_filtered_fft_int).T], axis=0, ignore_index=True)
        
        
    data_filtered_df.columns = df.columns
   
    data_filtered_df_diff = data_filtered_df.diff(axis=1)
    
    print(data_filtered_df_diff)
    
    data_filtered_df_diff = data_filtered_df_diff.apply(lambda x: normalize_minus_one_to_one(x), axis=1)
    data_filtered_df_diff = data_filtered_df_diff.apply(lambda x: x-np.mean(x), axis=1)
    data_filtered_df_diff.fillna(0, inplace=True)
    
    model = load_model_demo()
    X = data_filtered_df_diff
    

    predictions = model.predict(X)

    print(predictions)
    predicted_class = np.argmax(predictions, axis=1)
    dict= {0: 'Cube', 1: 'Cylinder', 2: 'Pentagon'}
    import tkinter as tk
    #tk window
    window = tk.Tk()
    window.title("Prediction")
    window.geometry("1200x800")
    img = tk.PhotoImage(file=rf"assets\{dict[predicted_class[0]]}.png")
    img_label = tk.Label(window, image=img)
    img_label.pack(side="bottom",fill="x", expand=1)
    label = tk.Label(window, text=f"{dict[predicted_class[0]]}", font=("Times New Roman", 120), fg="#0F3982")
    label.pack(side="bottom", fill="x", expand=1)
    window.mainloop()
    print(predicted_class)
    
        


def normalize_minus_one_to_one(array):
    return 2 * ((array - np.min(array)) / (np.max(array) - np.min(array))) - 1


def fft_filter(row, cutoff=0.07):
    # FFT der Zeile
    fft_coeffs = rfft(row)
    fft_freqs = rfftfreq(len(row))
    
    # Filter: Entfernen hochfrequenter Komponenten
    low_pass_filter = fft_freqs < cutoff
    filtered_fft_coeffs = fft_coeffs * low_pass_filter
    
    # Rücktransformation in den Zeitbereich
    filtered_row = irfft(filtered_fft_coeffs)
    return filtered_row


def load_model_demo():
    model = load_model('general_object_recognition.h5')
    return model


if __name__ == '__main__':
    # sensor_rotation = 1 -> sensor is rotated vertically, sensor_rotation = 0 -> sensor is rotated horizontally
    sender(password="jimmy4", angle=4, stop=False, runs=1, shape="pentagon", mode = "step", position = 13, sensor_rotation = 1, multi = False)
    listener()
    
    
    