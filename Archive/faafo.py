#%%
import random
import pandas as pd
import numpy as np
from defaults import MOVING_AVERAGE as ma


# Create a DataFrame with 100 columns and 100 rows of random values
df = pd.DataFrame(np.random.randint(0, 100, size=(100, 100)), columns=[f'col{i}' for i in range(100)])

# %%
df
# %%
def parse(path):
    # df = pd.read_csv(path)
    for x in range(len(df)-1):
        for y in range(a:=(len(df.columns)-1-ma)):
            sum = 0
            for i in range(ma):
                sum += df.iloc[x][y+i]
            df.iloc[x][y] = int(sum / ma)
# %%
parse("faf0")
df
# %%
