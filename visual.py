import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("new_log.txt")
df2 = pd.read_csv("claened_new_log.txt")
df3 = pd.read_csv("claened_claened_new_log.txt")



ax = plt.subplots(figsize = (16, 8))[1]
ax.plot(df.columns[:-1], df.iloc[0, :-1])
ax.plot(df2.columns[:-1], df2.iloc[0, :-1])
ax.plot(df3.columns[:-1], df3.iloc[0, :-1])
ax.set_ylim(0, 260)
ax.set_xticks([x for x in range(0, 73, 8)])
plt.show()

