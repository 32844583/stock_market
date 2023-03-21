import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from plotly.subplots import make_subplots
import talib   

stock = yf.Ticker("2330.TW")
data = stock.history(period='6mo')
data = data[['Open','High','Low','Close','Volume']]
data.reset_index(level='Date', inplace=True)



# https://stackoverflow.com/questions/61346100/plotly-how-to-style-a-plotly-figure-so-that-it-doesnt-display-gaps-for-missing
dt_all = pd.date_range(start=data['Date'].iloc[0],end=data['Date'].iloc[-1])
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(data['Date'])]
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    row_width=[0.2, 0.2, 0.4])


data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA5'] = data['Close'].rolling(window=5).mean()
fig.add_trace(go.Scatter(x=data['Date'],
                         y=data['MA5'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='MA 5',hoverinfo='skip'), row=1, col=1)
fig.add_trace(go.Scatter(x=data['Date'],
                         y=data['MA20'],
                         opacity=0.7,
                         line=dict(color='orange', width=2),
                         name='MA 20',hoverinfo='skip'), row=1, col=1)

# revise: candlestick + scatter 
cand = go.Figure(go.Candlestick(x=data['Date'],
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'],
                increasing_line_color = 'red',
                decreasing_line_color = 'green'))

data.loc[0:100:10, 'buy_sell'] = 'buy'
data.loc[0:100:27, 'buy_sell'] = 'sell'
# revise: buy_sell_point
fig.add_trace(
    go.Scatter(
        x=data.loc[0:100:10, 'Date'],
        y=data.loc[0:100:10, 'Close'],
        mode="markers",
        marker=dict(symbol='triangle-down', color='orange', line=dict(color='black',width=2), size = 10),
        text = '\n' + data['buy_sell'],
        textposition = 'middle right',
        name="buy"
    ), row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=data.loc[0:100:27, 'Date'],
        y=data.loc[0:100:27, 'Close'],
        mode="markers",
        marker=dict(symbol='triangle-up', color='lightskyblue', line=dict(color='black',width=2), size = 10),
        text =  + data['buy_sell'],
        textposition = 'middle right',
        name="sell"
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
fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors, name="volume"),
               secondary_y=False, row=2, col=1)

# revise: RSI
close = data['Close']
data['RSI'] = talib.RSI(close, timeperiod=14)
fig.add_trace(px.line(data, x="Date", y="RSI",
                 hover_name="Date", hover_data=["Date", "RSI"]).data[0],
              row=3, col=1)


fig.update_xaxes(
    rangebreaks=[dict(values=dt_breaks)]
)

fig.update_layout(
    autosize=False,
    width=800,
    height=800,
    )

fig.update_layout(xaxis_rangeslider_visible=False, 
                  xaxis3_rangeslider_visible=True, 
                  xaxis_type="date")

print(data['buy_sell'].value_counts())

fig.show()
# tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
# with tab1:
#     # Use the Streamlit theme.
#     # This is the default. So you can also omit the theme argument.
#     st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# with tab2:
#     # Use the native Plotly theme.
#     st.plotly_chart(fig, theme=None, use_container_width=True)