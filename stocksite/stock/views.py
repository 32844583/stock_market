from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf
import numpy as np
from json import loads, dumps
from django.views.decorators.csrf import csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def Canvas(request):
    stock = yf.Ticker("2330.TW")
    data = stock.history(period='6mo')
    data = data[['Open','High','Low','Close','Volume']]
    data.reset_index(level='Date', inplace=True)
    result = []
    for idx in range(data.shape[0]):
        # print(type())
        Date = data.iloc[idx, 0].date()
        Date = Date.strftime('%Y-%m-%d')
        Open = float(data.iloc[idx, 1])
        High = float(data.iloc[idx, 2])
        Low = float(data.iloc[idx, 3])
        Close = float(data.iloc[idx, 4])
        result.append({"date":Date, "open":Open, "high":High, "low":Low, "close":Close})

    result = dumps(result)
    context = {'stock_data':result}
    return render(request, "Canvas.html", context)





















period = '6mo'
third = 'RSI'

@csrf_exempt
def Graph(request):
    global third
    global period
    stock = yf.Ticker("2330.TW")
    data = stock.history(period=period)
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

    # candlestick
    cand = go.Figure(go.Candlestick(x=data['Date'],
                    open=data['Open'], high=data['High'],
                    low=data['Low'], close=data['Close'],
                    increasing_line_color = 'red',
                    decreasing_line_color = 'green'))

    fig.add_trace(cand.data[0], row=1, col=1)
    # ----------------------------------------------

    # buy_sell_point
    data.loc[0:2, 'buy_sell'] = 'buy'
    data.loc[2:4, 'buy_sell'] = 'sell'
    fig.add_trace(
        go.Scatter(
            x=data.loc[0:2, 'Date'],
            y=data.loc[0:2, 'Close'],
            mode="markers",
            marker=dict(symbol='triangle-down', color='orange', line=dict(color='black',width=2), size = 10),
            text = '\n' + data['buy_sell'],
            textposition = 'middle right',
            name="buy",
            hovertemplate='Price: %{y:$.2f} <extra></extra>'
        ), row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.loc[2:4, 'Date'],
            y=data.loc[2:4, 'Close'],
            mode="markers",
            marker=dict(symbol='triangle-up', color='lightskyblue', line=dict(color='black',width=2), size = 10),
            text =  + data['buy_sell'],
            textposition = 'middle right',
            name="sell",
            hovertemplate='Price: %{y:$.2f} <extra></extra>'
        ), row=1, col=1
    )
    # ----------------------------------------------

    # volume bar
    temp_vol = {'vol': data['Volume'].tolist(), 'last_vol': data['Volume'].shift(1).tolist()}
    temp_vol = pd.DataFrame(data=temp_vol)
    temp_vol = temp_vol.dropna()
    colors = ['red' if row['vol'] - row['last_vol'] >= 0
              else 'green' for index, row in temp_vol.iterrows()]
    colors.insert(0, 'green')
    
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors, name="volume"),
                   secondary_y=False, row=2, col=1)
    import talib
    data = data.assign(RSI=talib.RSI(data['Close']))

    fig.add_trace(px.line(data, x="Date", y="RSI",
                     hover_name="Date", hover_data=["Date", "RSI"]).data[0],
                  row=3, col=1)
    # ----------------------------------------------

    # layout setting
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


    context = {}
    context['graph'] = fig.to_html()


    if is_ajax(request=request):
        button_text = request.POST.get('button_text')
        if button_text == '3mo':
            period = '3mo'

        elif button_text == 'volume':
            third = 'volume'

        elif button_text == 'RSI':
            third = 'RSI'
            stock = yf.Ticker("2330.TW")
        data = stock.history(period=period)
        data = data[['Open','High','Low','Close','Volume']]
        data.reset_index(level='Date', inplace=True)
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
        cand = go.Figure(go.Candlestick(x=data['Date'],
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'],
                        increasing_line_color = 'red',
                        decreasing_line_color = 'green'))
        fig.add_trace(cand.data[0], row=1, col=1)
        data.loc[0:100:10, 'buy_sell'] = 'buy'
        data.loc[0:100:27, 'buy_sell'] = 'sell'
        fig.add_trace(
            go.Scatter(
                x=data.loc[0:100:10, 'Date'],
                y=data.loc[0:100:10, 'Close'],
                mode="markers",
                marker=dict(symbol='triangle-down', color='orange', line=dict(color='black',width=2), size = 10),
                text = '\n' + data['buy_sell'],
                textposition = 'middle right',
                name="buy",
                hovertemplate='Price: %{y:$.2f}<extra></extra>'
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
                name="sell",
                hovertemplate='Price: %{y:$.2f}<extra></extra>'
            ), row=1, col=1
        )
        temp_vol = {'vol': data['Volume'].tolist(), 'last_vol': data['Volume'].shift(1).tolist()}
        temp_vol = pd.DataFrame(data=temp_vol)
        temp_vol = temp_vol.dropna()
        colors = ['red' if row['vol'] - row['last_vol'] >= 0
                  else 'green' for index, row in temp_vol.iterrows()]
        colors.insert(0, 'green')
        
        fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors, name="volume"),
                       secondary_y=False, row=2, col=1)
        import talib
        data = data.assign(RSI=talib.RSI(data['Close']))
        if third == 'RSI':
            fig.add_trace(px.line(data, x="Date", y="RSI",
                         hover_name="Date", hover_data=["Date", "RSI"]).data[0],
                      row=3, col=1)
        else:
            fig = volume_design(fig, data, colors)
            
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
        djangotoajax = '0'+button_text
        newgraph = fig.to_html()
        return JsonResponse({'djangotoajax':djangotoajax, 'newgraph':newgraph}, status =200)

    return render(request, "Graph.html", context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') 


def volume_design(fig, data, colors):
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors, name="volume"),
                   secondary_y=False, row=3, col=1)
    return fig
