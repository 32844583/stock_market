import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from plotly.subplots import make_subplots

stock = yf.Ticker("2330.TW")
data = stock.history(period='6mo')
data = data[['Open','High','Low','Close','Volume']]
data.reset_index(level='Date', inplace=True)



# https://stackoverflow.com/questions/61346100/plotly-how-to-style-a-plotly-figure-so-that-it-doesnt-display-gaps-for-missing
dt_all = pd.date_range(start=data['Date'].iloc[0],end=data['Date'].iloc[-1])
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(data['Date'])]
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

fig = make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    row_width=[0.2, 0.2, 0.2, 0.4])


data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA5'] = data['Close'].rolling(window=5).mean()
fig.add_trace(go.Scatter(x=data['Date'],
                         y=data['MA5'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='MA 5'), row=1, col=1)
fig.add_trace(go.Scatter(x=data['Date'],
                         y=data['MA20'],
                         opacity=0.7,
                         line=dict(color='orange', width=2),
                         name='MA 20'), row=1, col=1)

# revise: candlestick + scatter 
cand = go.Figure(go.Candlestick(x=data['Date'],
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'],
                increasing_line_color = 'red',
                decreasing_line_color = 'green'))

# revise: buy_sell_point
fig.add_trace(
    go.Scatter(
        x=data.loc[0:100:10, 'Date'],
        y=data.loc[0:100:10, 'Close'],
        mode="markers",
        marker=dict(symbol='triangle-down', size = 12, color='black'),
        text = data['Open'],
        textposition = 'middle right'
    ), row=1, col=1
)

fig.add_trace(cand.data[0], row=1, col=1)

# volume bar

temp_vol = {'vol': data['Volume'].tolist(), 'last_vol': data['Volume'].shift(1).tolist()}
temp_vol = pd.DataFrame(data=temp_vol)
temp_vol = temp_vol.dropna()
colors = ['red' if row['vol'] - row['last_vol'] >= 0
          else 'green' for index, row in temp_vol.iterrows()]
colors.insert(0, 'green')
fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors),
               secondary_y=False, row=3, col=1)

# revise: RSI
fig.add_trace(px.line(data, x="Date", y="Close",
                 hover_name="Date", hover_data=["Date", "Low"]).data[0],
              row=4, col=1)


fig.update_xaxes(
    rangebreaks=[dict(values=dt_breaks)]
)
fig.show()