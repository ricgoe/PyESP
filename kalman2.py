import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

def dv_kalman(z):
    global A, H, Q, R, x, P, firstRun

    if firstRun is None:
        firstRun = 1
 
        A = np.array([[1, 1],
                      [0, 1]])
        H = np.array([1, 0])

        Q = np.array([[0.00007, 0],
                      [0, 0.003]])
        R = 0.09

        x = np.array([100, 0]).reshape(-1, 1)
        P =10000 * np.eye(2)

    # Kalman filter algorithm
    xp = A * x
    Pp = A * P * A.T + Q

    K = Pp * H.T / (H * Pp * H.T + R)

    x = xp + K * (z - H * xp)
    P = Pp - K * H * Pp

    pos = x[0, 0]
    delta_d = x[1, 0]
    Px = P

    return pos, delta_d, Px

# Beispielaufruf
firstRun = None  # Setze firstRun auf None, um die Initialisierung zu erzwingen


root = os.getcwd()
log_path = os.path.join(root, 'Logs')
file = os.path.join(log_path, f'{input("Shape: ")}_step_{input("Step size: ")}.csv')
df_data = pd.read_csv(file)

num_measurements = len(df_data.columns)-1
measurements = np.zeros(num_measurements)
kalman_outputs = np.zeros(num_measurements)



for i in range(len(df_data.columns)-1):
    measurement = df_data.iloc[40,i]
    result = dv_kalman(measurement)[0]
    measurements[i] = measurement
    kalman_outputs[i] = result




plt.plot(measurements, label='Messungen')
plt.plot(kalman_outputs, label='Kalman Filter Ausgabe')
plt.xlabel('Messung')
plt.ylabel('Wert')
plt.legend()
plt.title('Messungen und Kalman Filter Ausgabe')
plt.show()