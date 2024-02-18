from keras.models import load_model
import numpy as np
import pandas as pd

model = load_model('general_object_recognition.h5')

#df_test = pd.read_csv(r'Normalized_Data\scans_angle_2_8125_pos_10_rot_1_normalized.csv')
df_test = pd.read_csv(r'DEMO\scans_angle_demo.csv')

X = df_test.iloc[0]

X_reshaped = np.expand_dims(X.values, axis=0).astype('float32')

predicttions = model.predict(X_reshaped)
print(predicttions)
predicted_class = np.argmax(predicttions, axis=1)

print(predicted_class)