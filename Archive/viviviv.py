# %%
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

# %%
df = pd.read_csv("cleaned_triangle_step_2.csv").drop(columns=["shape"])

# %%
fig, ax = plt.subplots(figsize=(16, 8), subplot_kw={"projection": "polar"})
idx_numbers = [int(idx)*508/360 for idx in df.columns]
ax.scatter(idx_numbers, df.iloc[0,:])

# %%
plt.show()

# %%



