#LANCE

#Import Libraries 
import urllib3
import json
import pandas as pd
import datetime
import numpy as np
from sklearn.neural_network import MLPRegressor

pd.set_option('display.max_rows',250)
pd.set_option('display.max_columns',10)
pd.set_option('display.width', 1000)


#Handle GET call
def request(url):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    r = http.request('GET',url)
    data = json.loads(r.data)
    return data["Data"]

def build_dataset2():
    data = request("https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&e=bitfinex&limit=2000")
    dic = {}
    date_col = []
    close_col = []
    open_col = []
    volume_from_col = []
    volume_to_col = []
    high_col = []
    low_col = []
    for item in data:
        ts = item["time"]
        close = item["close"]
        open = item["open"]
        volume_from = item["volumefrom"]
        volume_to = item["volumeto"]
        high = item["high"]
        low = item["low"]
        date_col.append(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        close_col.append(close)
        open_col.append(open)
        volume_from_col.append(volume_from)
        volume_to_col.append(volume_to)
        high_col.append(high)
        low_col.append(low)
    dic["Date"] = date_col
    dic["Close"] = close_col
    dic["Open"] = open_col
    dic["VolumeFrom"] = volume_from_col
    dic["VolumeTo"] = volume_to_col
    dic["High"] = high_col
    dic["low"] = low_col
    df = pd.DataFrame(data=dic)
    return(df)
    
    

df = build_dataset2()


def get_RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
         pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)


#sample data from StockCharts

RSI = get_RSI(df.Close, 14 )

df["RSI"] = RSI











#Other (Code Storage)

#print(datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S'))
###Get BTC/USD Price
##def get_price(ts):
##    url = "https://min-api.cryptocompare.com/data/pricehistorical?fsym=BTC&e=Bitfinex&tsyms=USD&ts="
##    url = url + str(ts)
##    data = request(url)
##    price = data["BTC"]
##    return price["USD"]
##
##
###Building The dataset
##def build_dataset():
##    dic = {}
##    date_col = []
##    price_col = []
##    count = 0
##    for i in range(1518286883,1517386883,-900):
##        count = count +1
##        print(count)
##        price = get_price(i)
##        date = datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
##        price_col.append(price)
##        date_col.append(date)
##    dic["Date"] = date_col
##    dic["Price"] = price_col
##    df = pd.DataFrame(data=dic)
##    return(df)

#df = build_dataset()

###Preprocessing
##class_high = df['High'].tolist()
##df = df.drop('High', 1)
##df = df.drop('Date', 1)
##matrix = df.values.tolist()
##x=matrix
##y=class_high
##
##print(df)
##print(y)
##
###Sklearn MLPRegressor
##clf = MLPRegressor()
##clf.fit(x, y) 
##
##
##k= clf.predict([[10754.00,10777.00,589.76,6341405.43,10710.00]])
