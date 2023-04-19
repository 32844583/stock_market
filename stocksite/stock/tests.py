import pandas as pd
import yfinance as yf
import numpy as np
from json import loads, dumps
from datetime import datetime
import plotly.graph_objs as go

fig = go.Figure()

# Add some traces to the figure
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], name="trace1"))
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[7, 8, 9], name="trace2"))

# Delete a trace by name
fig.delete_traces("trace1")

# Show the updated figure
fig.show()
# https://plainenglish.io/blog/user-registration-and-login-authentication-in-django-2f3450479409#viewspy
# ---
# python plotly update particular trace's data by go

# import plotly.graph_objects as go
# import numpy as np

# x = np.random.randn(500)
# y1 = np.random.randn(500)
# y2 = np.random.randn(500)

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=x, y=y1, mode='markers', name='Trace 1'))
# fig.add_trace(go.Scatter(x=x, y=y2, mode='markers', name='Trace 2'))

# fig.show()

# # Update trace data for Trace 1
# new_y1 = np.random.randn(500)

# fig.update_traces(selector=dict(name='Trace 1'), y=new_y1)

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



# # 計算 KD 黃金交叉、死亡交叉欄位
# df['KD_Golden_Cross'] = ((df['K'].shift(1) < df['D'].shift(1)) & (df['K'] > df['D'])).astype(int)
# df['KD_Death_Cross'] = ((df['K'].shift(1) > df['D'].shift(1)) & (df['K'] < df['D'])).astype(int)

# # 刪除缺失值
# df = df.dropna()

# # 顯示結果
# print(df.tail())


