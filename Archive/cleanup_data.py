import pandas as pd
from defaults import MOVING_AVERAGE as ma

# df = pd.DataFrame(np.random.randint(0, 100, size=(100, 100)), columns=[f'col{i}' for i in range(100)])
ma += 6
# def parse(path):
#     df = pd.read_csv(path)
#     for x in range(len(df)):
#         for y in range(a:=(len(df.columns)-1-ma)):
#             sum = 0
#             for i in range(ma):
#                 sum += df.iloc[x, y+i]
#             df.iloc[x, y] = int(sum / ma)
#     df.to_csv("cleaned_"+path, index=False)


def parse(path):
    df = pd.read_csv(path)
    for x in range(len(df)):
        for y in range(a:=(len(df.columns)-1-ma)):
            window = df.iloc[x, y:y+ma]
            df.iloc[x, y] = int(window.mean())
    df.to_csv("cleaned_"+path, index=False)