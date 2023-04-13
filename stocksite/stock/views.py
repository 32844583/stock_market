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
import talib
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


















data=0
dt_breaks=0
colors=0
stock_name="2330.TW"
interval='1d'
period='6mo'
third='RSI'
fig =''
@csrf_exempt
def Graph(request):
    global fig, period, third, interval
    # https://stackoverflow.com/questions/61346100/plotly-how-to-style-a-plotly-figure-so-that-it-doesnt-display-gaps-for-missing
    data_reload_recalculate()
    initialize()
    first_graph_generate()
    buy_sell_point_graph()
    second_graph_generate()
    third_graph_generate()
    update_layout()

    context = {}
    context['graph'] = fig.to_html()


    if is_ajax(request=request):
        eventName = request.POST.get('eventName')
        button_text = request.POST.get('button_text')

        if 'mo' in button_text:
            period = button_text
        elif 'd' in button_text:
            interval = button_text
        else:
            third = button_text

        # if eventName == 'ajax-hover-event':
        #     fig.add_trace(
        #         go.Scatter(
        #             x=data.loc[2:4, 'Date'],
        #             y=data.loc[2:4, 'Close'],
        #             mode="markers",
        #             marker=dict(
        #                 symbol='triangle-up', 
        #                 color='lightskyblue', 
        #                 line=dict(color='black',width=2), 
        #                 size = 10,
        #                 opacity=0.5),
        #             text =  + data['buy_sell'],
        #             textposition = 'middle right',
        #             name="sell",
        #             hovertemplate='Price: %{y:$.2f} <extra></extra>'
        #         ), row=1, col=1
        #     )

        if eventName == 'ajax-period-event' or eventName == 'ajax-interval-event':
            data_reload_recalculate()
            initialize()
            first_graph_generate()
            buy_sell_point_graph()
            second_graph_generate()
            third_graph_generate()
            update_layout()
        else:
            third_graph_update()
        # data.loc[0:100:10, 'buy_sell'] = 'buy'
        # data.loc[0:100:27, 'buy_sell'] = 'sell'
        # fig.add_trace(
        #     go.Scatter(
        #         x=data.loc[0:100:10, 'Date'],
        #         y=data.loc[0:100:10, 'Close'],
        #         mode="markers",
        #         marker=dict(symbol='triangle-down', color='orange', line=dict(color='black',width=2), size = 10),
        #         text = '\n' + data['buy_sell'],
        #         textposition = 'middle right',
        #         name="buy",
        #         hovertemplate='Price: %{y:$.2f}<extra></extra>'
        #     ), row=1, col=1
        # )
        # fig.add_trace(
        #     go.Scatter(
        #         x=data.loc[0:100:27, 'Date'],
        #         y=data.loc[0:100:27, 'Close'],
        #         mode="markers",
        #         marker=dict(symbol='triangle-up', color='lightskyblue', line=dict(color='black',width=2), size = 10),
        #         text =  + data['buy_sell'],
        #         textposition = 'middle right',
        #         name="sell",
        #         hovertemplate='Price: %{y:$.2f}<extra></extra>'
        #     ), row=1, col=1
        # )
        djangotoajax = '0'+button_text
        newgraph = fig.to_html()
        return JsonResponse({'djangotoajax':djangotoajax, 'newgraph':newgraph}, status =200)

    
    trades = []
    for i in range(4):
        trades.append({'index':i, 'code': '2888', 'quantity': 0, 'pnl': -2.0, 'date': '2023-03-29', 'price': 8.31, 'reason': 'est'})
    # trades = pd.DataFrame(trades)
    context['trades'] = trades

    return render(request, "Graph.html", context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH')

def clear_graph(n):
    global fig
    fig.update_traces(name=n, remove=True)


def volume_design(fig, data, colors):
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors, name="volume"),
                   secondary_y=False, row=3, col=1)
    return fig

def initialize():
    global fig
    fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.1,
                            row_width=[0.2, 0.2, 0.4])



def update_layout():
    global fig, dt_breaks
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

def first_graph_generate():
    global data, fig
    fig.add_trace(go.Candlestick(x=data['Date'],
                open=data['Open'], 
                high=data['High'],
                low=data['Low'], 
                close=data['Close'],
                increasing_line_color = 'red',
                decreasing_line_color = 'green',
                name='Candlestick'), row=1, col=1)

    fig.add_trace(go.Scatter(x=data['Date'],
                             y=data['MA5'],
                             opacity=0.7,
                             line=dict(color='blue', width=2),
                             hoverinfo='skip',
                             name='ma5'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data['Date'],
                             y=data['MA20'],
                             opacity=0.7,
                             line=dict(color='orange', width=2),
                             hoverinfo='skip',
                             name='ma20'), row=1, col=1)

def buy_sell_point_graph():
    global data, colors, fig
    data.loc[0:2, 'buy_sell'] = 'buy'
    data.loc[2:4, 'buy_sell'] = 'sell'
    fig.add_trace(
        go.Scatter(
            x=data.loc[0:2, 'Date'],
            y=data.loc[0:2, 'Close'],
            mode="markers",
            marker=dict(
                symbol='triangle-down', 
                color='orange', 
                line=dict(color='black',width=2), 
                size = 10,
                opacity=0.5),
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
            marker=dict(
                symbol='triangle-up', 
                color='lightskyblue', 
                line=dict(color='black',width=2), 
                size = 10,
                opacity=0.5),
            text =  + data['buy_sell'],
            textposition = 'middle right',
            name="sell",
            hovertemplate='Price: %{y:$.2f} <extra></extra>'
        ), row=1, col=1
    )

def second_graph_generate():
    global data, colors, fig
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color=colors, name="volume"),
                   secondary_y=False, row=2, col=1)

def third_graph_generate():
    global data, fig, third
    fig.add_trace(go.Scatter(x=data['Date'], y=data[third],
                    mode='lines',
                    name='third'), row=3, col=1)
def third_graph_update():
    global fig, third, data
    fig.update_traces(selector=dict(name='third'), y=data[third])

def data_reload_recalculate():
    global data, interval, period, stock_name, dt_breaks
    print('function', period)
    stock = yf.Ticker(stock_name)
    data = stock.history(period=period, interval=interval)
    data = data[['Open','High','Low','Close','Volume']]
    data.reset_index(level='Date', inplace=True)
    dt_all = pd.date_range(start=data['Date'].iloc[0],end=data['Date'].iloc[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(data['Date'])]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]


    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA5'] = data['Close'].rolling(window=5).mean()

    # RSI
    data = data.assign(RSI=talib.RSI(data['Close']))
    
    # K
    high = data['High'].values
    low = data['Low'].values
    close = data['Close'].values
    k, d = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    data['K'] = k
    data['D'] = d

    # volume bar
    temp_vol = {'vol': data['Volume'].tolist(), 'last_vol': data['Volume'].shift(1).tolist()}
    temp_vol = pd.DataFrame(data=temp_vol)
    temp_vol = temp_vol.dropna()
    colors = ['red' if row['vol'] - row['last_vol'] >= 0
              else 'green' for index, row in temp_vol.iterrows()]
    colors.insert(0, 'green')
    print(data.shape)
