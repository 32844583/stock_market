import pandas as pd
import yfinance as yf
import numpy as np
from json import loads, dumps
from datetime import datetime




# import plotly.graph_objects as go
# import numpy as np

# x = np.random.randn(500)
# y = np.random.randn(500)

# fig = go.Figure(data=go.Scatter(
#     x=x,
#     y=y,
#     mode='markers',
#     marker=dict(
#         size=16,
#         color=np.random.randn(500),
#         colorscale='Viridis',
#         showscale=True
#     )
# ))

# fig.show()

# # Update trace data
# new_x = np.random.randn(500)
# new_y = np.random.randn(500)

# fig.update_traces(x=new_x, y=new_y)

# fig.show()



















# ------------------------------------------------------
# import pandas as pd
# import yfinance as yf

# # 從 yfinance 取得股票收盤價
# df = yf.download("AAPL", start="2021-01-01", end="2022-04-10")

# # 計算 20、60、120 日均線
# df['MA20'] = df['Close'].rolling(window=20).mean()
# df['MA60'] = df['Close'].rolling(window=60).mean()
# df['MA120'] = df['Close'].rolling(window=120).mean()

# # 新增 Bullish 欄位，預設值為 False
# df['Bullish'] = False

# # 判斷是否為多頭排列，並更新 Bullish 欄位的值
# for i in range(120, len(df)):
#     ma20 = df.iloc[i]['MA20']
#     ma60 = df.iloc[i]['MA60']
#     ma120 = df.iloc[i]['MA120']
#     if ma20 > ma60 and ma60 > ma120:
#         df.at[df.index[i], 'Bullish'] = True

# # 印出結果
# print(df.tail())
# ------------------------------------------------------
# import pandas as pd
# import yfinance as yf
# import talib

# # 下載歷史股價資料
# df = yf.download('AAPL', start='2021-01-01', end='2022-04-10')

# # 計算 KD 值
# high = df['High'].values
# low = df['Low'].values
# close = df['Close'].values
# k, d = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

# # 將 KD 值新增為新欄位
# df['K'] = k
# df['D'] = d

# # 計算 KD 黃金交叉、死亡交叉欄位
# df['KD_Golden_Cross'] = ((df['K'].shift(1) < df['D'].shift(1)) & (df['K'] > df['D'])).astype(int)
# df['KD_Death_Cross'] = ((df['K'].shift(1) > df['D'].shift(1)) & (df['K'] < df['D'])).astype(int)

# # 刪除缺失值
# df = df.dropna()

# # 顯示結果
# print(df.tail())


