import shioaji as sj
import pandas as pd
import talib
import requests
import time
import os
import csv
from datetime import datetime, date, timedelta

startdate = (date.today() + timedelta(days=-5)).strftime("%Y-%m-%d")
# print(startdate)
Buystock = 0
Sellstock = 0
SellD = 0
SellU = 0
buyD = 0
buyU = 0
SellDs = 0
SellUs = 0
buyDs = 0
buyUs = 0
Openner = 0
token = '4cwTgoUM0Npnnob1D0aUHCYWxN6huiqVF9poI0G1Efe'


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


today = time.strftime('%y%m', time.localtime())
pathtoday = str(r'C:\_Phil\Private\stockprice\Log_' + today + '.csv')
if os.path.isfile(pathtoday):
    pass
else:
    with open(pathtoday, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['dateTime', 'Point1', 'Point2', 'difference', 'TWD'])
api = sj.Shioaji(simulation=True)  # 模擬模式
api.login(api_key="H6WLFjAN6QaRKucnGBm9TgEGpghBNNhafRyj3xjMLp7M",
          secret_key="HRgYZfKx7fz2BFYgxxcdxWvtXpCMYPj6BgsqySArEdmF",
          fetch_contract=False)

api.fetch_contracts(contract_download=True)

contracts = [api.Contracts.Futures.MXF['MXF202308']]
today = time.strftime('%Y-%m-%d')

enddate = today  # 結束日期

LastTI = 0

while True:
    inTI = time.time()
    snapshots = api.snapshots(contracts)
    if inTI - LastTI >= 60:
        kbars = api.kbars(
            contract=api.Contracts.Futures.MXF['MXF202308'],
            start=startdate, end=enddate
        )
        # 將Tick數據轉換為DataFrame
        df = pd.DataFrame({**kbars})
        df.ts = pd.to_datetime(df.ts)
        df.head(20)
        # 計算布林通道指標
        df['MA'] = talib.SMA(df['Close'], timeperiod=100)  # 計算20日移動平均線
        df['STD'] = talib.STDDEV(df['Close'], timeperiod=100)  # 計算20日收盤價的標準差
        df['Upper'] = df['MA'] + 2 * df['STD']  # 計算布林通道上軌
        df['Lower'] = df['MA'] - 2 * df['STD']  # 計算布林通道下軌

        # 計算隨機指標
        df['K'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=100)[0]  # 計算K值
        df['D'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=100)[1]  # 計算D值

        if Buystock == 0 & Sellstock == 0:
            if (df['K'].tail(1).values > 60 & df['D'].tail(1).values > 60 & df['Close'].tail(1).values > df['MA'].tail(1).values):
                now = datetime.now()
                current_time = now.strftime("%y%m%d %H:%M:%S")
                print("Current Time =", current_time, "B ")
                Buystock += 1
                message = '%s %s %s' % (current_time, "B ", snapshots[0].close)
                lineNotifyMessage(token, message)
                Buypoint = snapshots[0].close

            if (df['K'].tail(1).values < 40 & df['D'].tail(1).values < 40 & df['Close'].tail(1).values < df['MA'].tail(1).values):
                now = datetime.now()
                current_time = now.strftime("%y%m%d %H:%M:%S")
                print("Current Time =", current_time, "S ")
                Sellstock += 1
                message = '%s %s %s' % (current_time, "S ", snapshots[0].close)
                lineNotifyMessage(token, message)
                Sellpoint = snapshots[0].close

        if Buystock == 1:
            if (df['K'].tail(1).values > df['D'].tail(1).values):
                SellU = 1
            if (df['K'].tail(1).values < df['D'].tail(1).values) & (
                df['Close'].tail(1).values > df['MA'].tail(1).values) & SellU == 1:
                SellUs = 2
            else:
                SellUs = 0
            if SellUs == 2:
                now = datetime.now()
                current_time = now.strftime("%y%m%d %H:%M:%S")
                print("Current Time =", current_time, "S ")
                Sellstock += 1
                Sellpoint = snapshots[0].close
                earn = (Buypoint - Sellpoint) * 50
                message = '%s %s %s %s' % (current_time, "B ", snapshots[0].close, earn)
                lineNotifyMessage(token, message)
        if Sellstock == 1:
            if (df['K'].tail(1).values < df['D'].tail(1).values):
                buyD = 1
            if (df['K'].tail(1).values > df['D'].tail(1).values) & (df['Close'].tail(1).values < df['MA'].tail(1).values) & buyD == 1:
                buyDs = 2
            else:
                buyDs = 0
            if buyDs == 2:
                now = datetime.now()
                current_time = now.strftime("%y%m%d %H:%M:%S")
                print("Current Time =", current_time, "B ")
                Buystock += 1
                message = '%s %s %s' % (current_time, "B ", snapshots[0].close)
                lineNotifyMessage(token, message)
                Buypoint = snapshots[0].close
                buyU = 0
        print(df['K'].tail(1).values, df['D'].tail(1).values, df['Lower'].tail(1).values, df['MA'].tail(1).values,
              df['Upper'].tail(1).values, df['Close'].tail(1).values)
        LastTI = time.time()