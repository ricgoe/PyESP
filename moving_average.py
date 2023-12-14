import pandas as pd
from defaults import MOVING_AVERAGE as ws
import os

#Moving Average
def moving_average():
    path_to_get = os.path.join(os.getcwd(), 'Logs')
    path_to_push = os.path.join(os.getcwd(), 'Cleaned_Logs')
    files_to_get = os.listdir(path_to_get)
    
    for file in files_to_get:
        df = pd.read_csv(file)
        df_cleaned = pd.DataFrame()
        window_size = ws
        for x in range(len(df)):
            time_series = df.iloc[x, :-1]
            moving_average_time_series = round(time_series.rolling(window = window_size).mean())
            df_cleaned = pd.concat([df_cleaned, moving_average_time_series], axis = 1)
        df_cleaned = df_cleaned.T
        df_cleaned[len(df.columns)-1] = df['shape']
        df_cleaned.columns = df.columns
        df_cleaned.to_csv(os.path.join(path_to_push, 'cleaned_'+file), index=False)