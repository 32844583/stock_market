import yfinance as yf
import json
import plotly.graph_objs as go
from flask import Flask, jsonify, render_template, session, request
import datetime
import pandas as pd

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        timeframe = request.form['timeframe']
    else:
        timeframe = '3mo'
    # 獲取台灣股票代號為 2330 的股票資訊
    stock = yf.Ticker("2330.TW")

    # 獲取股票的歷史價格資料
    data = stock.history(period=timeframe)
    data.reset_index(level='Date', inplace=True)


    # 創建買賣點 DataFrame
    buy_sell_points = pd.DataFrame({
        'Date': ['2023-03-06', '2023-03-07', '2023-03-08', '2023-03-09', '2023-03-10'],
        'Type': ['Buy', 'Sell', 'Buy', 'Sell', 'Buy'],
        'Reason': ['RSI指標超賣', 'MACD 交叉', '5日線上揚', '10日線上揚', '20日線上揚']
    })

    buy_sell_points['Date'] = pd.to_datetime(buy_sell_points['Date']).dt.tz_localize('Asia/Taipei')
    buy_sell_points = buy_sell_points.merge(data[["Date", "Close"]], how='inner', on='Date')
    buy_sell_points.rename(columns={'Close':'Price'}, inplace=True)

    # 創建買賣點散點圖
    buy_points = buy_sell_points[buy_sell_points['Type'] == 'Buy']
    sell_points = buy_sell_points[buy_sell_points['Type'] == 'Sell']
    buy_scatter = go.Scatter(x=buy_points['Date'], y=buy_points['Price'],
                             mode='markers',
                             marker=dict(size=10, symbol='triangle-up', color='black'),
                             name='Buy',
                             text=buy_points['Reason'])
    sell_scatter = go.Scatter(x=sell_points['Date'], y=sell_points['Price'],
                              mode='markers',
                              marker=dict(size=10, symbol='triangle-down', color='black'),
                              name='Sell',
                              text=sell_points['Reason'])

    # 使用 Plotly 繪製 K 線圖
    candlestick = go.Candlestick(x=data['Date'],
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                line=dict(
                                    width=1,
                                ))
    # 創建成交量柱狀圖
    volume_bar = go.Bar(x=data['Date'], y=data['Volume'], name='Volume', yaxis='y2')
    # 設定適當的 y 軸範圍，避免成交量 bar 與 candlestick 圖表重疊
    y_range = [data['Low'].min() * 0.8, data['High'].max() * 1.2]
    volume_range = [0, data['Volume'].max() * 4]
    # 調整 bar 間距
    x_tickvals = data['Date'].iloc[::10]
    x_tickformat = "%m/%d"
    layout = go.Layout(
        xaxis=dict(
            type="category",
            tickmode="array",
            tickvals=x_tickvals,
            tickformat=x_tickformat,
            showticklabels=False,
        ),
        yaxis=dict(
            title="Price",
            range=y_range
        ),
        yaxis2=dict(
            title="Volume",
            range=volume_range,
            overlaying="y",
            side="right",
            showgrid=False,
            domain=[0, 1]
        ),
        height=600,
        xaxis_rangeslider_visible=False,
        margin=dict(l=0, r=50, b=0, t=50, pad=4),
        width=800,

    )
    fig = go.Figure(data=[candlestick, volume_bar, buy_scatter, sell_scatter], layout=layout)
    fig.update_traces(line=dict(width=1), selector=dict(type='candlestick'))
    
    # 調整成交量柱狀圖顏色

    colors = []
    for i in range(len(data)):
        if i != 0:
            if data['Close'][i] > data['Close'][i-1]:
                colors.append('green')
            else:
                colors.append('red')
        else:
            colors.append('black')
    volume_bar.marker.color = colors

    # 將圖表轉換為 HTML 代碼
    plot_html = fig.to_html(full_html=False)


    session['balance'] = 1000
    balance = session.get('balance', 1000)
    return render_template('index.html', balance=balance, plot_html=plot_html)

@app.route('/search_stock', methods=['POST'])
def search_stock():

    stock_id = request.form['stock_id'] + '.TW'

    price = yf.Ticker("MSFT").fast_info['lastPrice']
    # hist = msft.history(period="1mo")

    

    session['current_stock'] = {'stock_id': stock_id, 'price': price}
    return jsonify({'price': price, 'can_order': True})

@app.route('/history')
def history():
    transaction_history = session.get('transaction_history', [])
    return render_template('history.html', transaction_history=transaction_history)

@app.route('/place_order', methods=['POST'])
def place_order():
    order_quantity = int(request.form['order_quantity'])
    current_stock = session.get('current_stock', None)
    if current_stock is None:
        return jsonify({'error': '查無此股票'})
    else:
        stock_id = current_stock['stock_id']
        price = current_stock['price']
        total_price = order_quantity * price
        # 檢查餘額是否足夠
        balance = session.get('balance', 1000)
        if total_price > balance:
            return jsonify({'error': '餘額不足'})
        else:
            # 更新餘額
            session['balance'] = balance - total_price
            # 記錄交易資訊
            transaction_info = '下單成功：股票代號 {}, 下單數量 {}, 總價格 {}'.format(stock_id, order_quantity, total_price)
            transaction_history = session.get('transaction_history', [])
            transaction_history.append(transaction_info)
            session['transaction_history'] = transaction_history
            # 回傳交易資訊和更新後的餘額
            return jsonify({'transaction_info': transaction_info, 'balance': session['balance']})

if __name__ == '__main__':
    app.run(debug=True)
