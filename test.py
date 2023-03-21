import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import pandas as pd
import yfinance as yf
from datetime import datetime
import matplotlib.dates as dates
import mplfinance as mpf
from matplotlib.pyplot import figure
from babel.dates import format_date, format_datetime, format_time
stock = yf.Ticker("2330.TW")
data = stock.history(period='3mo')
data = data[['Open','High','Low','Close','Volume']]
# data.index = data.index.strftime('%b-%d')
dates = data.index.strftime("%Y-%d-%b")
dates = pd.to_datetime(dates, format='%Y-%d-%b')
temp = []
for i in range(1,5):
    temp.append(format_date(dates[i], locale='en'))
# print(data.index[0].date)
print(temp)
PM_25 = data.Close.tolist()
names = np.array([str(i)+str(j) for i, j in zip(temp[0:4:2], PM_25[1:5:2])])
fig, ax = plt.subplots(figsize=(8, 6))
sc = plt.scatter(temp[0:4:2], PM_25[1:5:2])

mpf.plot(data ,type='candle', returnfig=True, ax=ax)
c = np.random.randint(1,5,size=15)

norm = plt.Normalize(1,4)
cmap = plt.cm.RdYlGn

# ax[0].scatter(, s=100)
# ax[0].scatter(dates[5:10], PM_25[5:10], s=100)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)
# print(dates[0:10], PM_25[0:10])
def update_annot(ind):
    
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                           " ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)
    

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)
# fig, axlist = mpf.plot(data ,type='candle', returnfig= True)
# axlist[0].set_xticklabels(dates, ha='left')
# temp = data.index.date.strftime('%b-%d')
# temp = ['2023-02-15', '2023-02-16', '2023-02-17', '2023-02-20']
# temp = []
# for i in data.index:
#     temp.append(i.strftime('%b-%d'))
# temp = pd.to_datetime(temp, format='%b-%d')
# print(temp)
# plt.xticks(np.arange(0,len(temp),1), temp)
# ax[0].set_ylim(500,600)
plt.show()
