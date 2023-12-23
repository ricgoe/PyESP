import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

def dv_kalman(z):
    global A, H, Q, R, x, P, firstRun

    if firstRun is None:
        firstRun = 1
 
        # A = np.array([[1, 1],
        #               [0, 1]])
        # H = np.array([1, 0])

        # Q = np.array([[1*(10**-5), 0],
        #               [0, 0.003]])
        # R = 2.92*(10**-3)

        # x = np.array([100, 0]).reshape(-1, 1)
        # P = 100 * np.eye(2)
        
        
        A = np.matrix([[1.]])
        #B = np.matrix([[0.]])
        H = np.matrix([[1.]])
        Q = np.matrix([[0.00001]])
        R = np.matrix([[2.92*(10**-3)]])
        
        x = np.matrix([[0.]])      # initial distance estimate
        P = np.matrix([[1000.]])

    # Kalman filter algorithm
    xp = A * x
    Pp = A * P * A.T + Q

    K = Pp * H.T / (H * Pp * H.T + R)

    x = xp + K * (z - H * xp)
    P = Pp - K * H * Pp

    #pos = x[0, 0]
    delta_d = 0#x[1, 0]
    pos = x
    
    Px = P

    return pos, delta_d, Px

# Beispielaufruf
firstRun = None  # Setze firstRun auf None, um die Initialisierung zu erzwingen


root = os.getcwd()
log_path = os.path.join(root, 'Logs')
#log_path = os.path.join(root, 'Study')
file = os.path.join(log_path, f'{input("Shape: ")}_step_{input("Step size: ")}.csv')
#file = os.path.join(log_path, f'Run_{input("Run: ")}_step_1.csv')
df_data = pd.read_csv(file)

num_measurements = len(df_data.columns)-1
measurements = np.zeros(num_measurements)
kalman_outputs = np.zeros(num_measurements)



for i in range(len(df_data.columns)-1):
    measurement = df_data.iloc[20,i]
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