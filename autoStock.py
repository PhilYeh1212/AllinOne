import shioaji as sj
import pandas as pd
import numpy as np
import talib
import requests
import time
import csv
from datetime import datetime, date, timedelta
from shioaji import TickFOPv1, Exchange

startdate = (date.today() + timedelta(days=-5)).strftime("%Y-%m-%d")
# print(startdate)
Buystock = 0
Sellstock = 0
sellD = 0
sellU = 0
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
# if os.path.isfile(pathtoday):
#     pass
# else:
#     with open(pathtoday, 'a+', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['dateTime', 'Point1', 'Point2', 'difference', 'TWD'])
api = sj.Shioaji(simulation=True)  # 模擬模式
api.login(api_key="H6WLFjAN6QaRKucnGBm9TgEGpghBNNhafRyj3xjMLp7M",
          secret_key="HRgYZfKx7fz2BFYgxxcdxWvtXpCMYPj6BgsqySArEdmF",
          fetch_contract=False)

api.fetch_contracts(contract_download=True)
# print(api.Contracts)
contracts = [api.Contracts.Futures.MXF['MXF202310']]
today = time.strftime('%Y-%m-%d')
# print(today)
symbol = "TXFF"
enddate = today

# def quote_callback(exchange:Exchange, tick:TickFOPv1):
#     dftick = pd.DataFrame({**tick})
#     dftick.ts = pd.to_datetime(dftick.ts)
#     dftick.tail(5)
#     print(dftick)

# api.quote.subscribe(
#     api.Contracts.Futures.MXF['MXF202307'],
#     quote_type=sj.constant.QuoteType.Tick,
#     version=sj.constant.QuoteVersion.v1
# )
LastTI = 0

while True:
    inTI = time.time()
    # for i in range(0, 12):
    # price = dftick['amount'].tail(1).values/dftick['volume'].tail(1).values
    # print(price)
    snapshots = api.snapshots(contracts)
    if inTI - LastTI >= 60:
        kbars = api.kbars(
            contract=api.Contracts.Futures.MXF['MXF202310'],
            start=startdate, end=enddate
        )
        # 將Tick數據轉換為DataFrame
        df = pd.DataFrame({**kbars})
        df.ts = pd.to_datetime(df.ts)
        df.head(20)

        df['MA'] = talib.SMA(df['Close'], timeperiod=18)
        df['MACD'], df['Signal_Line'], _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=12)
        df['STD'] = talib.STDDEV(df['Close'], timeperiod=18)
        df['Upper'] = df['MA'] + 2 * df['STD']
        df['Lower'] = df['MA'] - 2 * df['STD']
        df['K'], df['D'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3, slowd_period=3)
        df['J'] = 3 * df['K'] - 2 * df['D']
        # if (df['K'].tail(1).values > 20) & (df['Close'].tail(1).values > df['Lower'].tail(1).values):

        if (df['K'].tail(1).values < df['D'].tail(1).values) & (df['J'].tail(1).values > 0) & (Buystock == 0) & (df['Close'].tail(1).values < df['Lower'].tail(1).values) &(df['MACD'].tail(1).values > df['Signal_Line'].tail(1).values):
            buyU = 2
        elif (df['K'].tail(1).values > df['D'].tail(1).values) & (df['J'].tail(1).values < 0) & (df['Close'].tail(1).values > df['MA'].tail(1).values) &(df['MACD'].tail(1).values < df['Signal_Line'].tail(1).values):
            sellU = 2

        if (df['K'].tail(1).values > df['D'].tail(1).values) & (df['J'].tail(1).values < 0) & (Sellstock == 0) & (df['Close'].tail(1).values > df['MA'].tail(1).values) &(df['MACD'].tail(1).values < df['Signal_Line'].tail(1).values):
            sellD = 2
        if (df['K'].tail(1).values < df['D'].tail(1).values) & (df['J'].tail(1).values > 0) & (df['Close'].tail(1).values < df['Lower'].tail(1).values) &(df['MACD'].tail(1).values > df['Signal_Line'].tail(1).values):
            buyD = 2
        # df['Signal'] = df['BuySignal'] + df['SellSignal']


        # signal = row['Signal']
        # close = row['Close']
        # print(signal, close)
        if buyU == 2 and Buystock == 0:
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "B ")
            Buystock += 1
            message = '%s %s %s' % (current_time, "B ", snapshots[0].close)
            lineNotifyMessage(token, message)
            buyU = 0
            # order = api.insert_order(
            #     symbol=symbol,
            #     price=close,
            #     action=sj.constant.Action.Buy,
            #     price_type=sj.constant.TFTOrderPriceType.LMT,
            #     order_type=sj.constant.TFTOrderType.ROD,
            #     quantity=1,
            # )
            # positions.append(order)
        if sellU == 2 and Buystock == 1:
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "S ")
            message = '%s %s %s' % (current_time, "S ", snapshots[0].close)
            lineNotifyMessage(token, message)
            Buystock -= 1
            # order = api.insert_order(
            #     symbol=symbol,
            #     price=close,
            #     action=sj.constant.Action.Sell,
            #     price_type=sj.constant.TFTOrderPriceType.LMT,
            #     order_type=sj.constant.TFTOrderType.ROD,
            #     quantity=1,
            # )
            # api.update_status([order])
        if sellD == 2 and Buystock == 0:
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "S ")
            message = '%s %s %s' % (current_time, "S ", snapshots[0].close)
            lineNotifyMessage(token, message)
            Buystock += 1

        if buyD == 2 and Buystock == 1:
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "B ")
            Buystock -= 1
            message = '%s %s %s' % (current_time, "B ", snapshots[0].close)
            lineNotifyMessage(token, message)
            buyU = 0
        print(df['K'].tail(1).values, df['D'].tail(1).values, df['J'].tail(1).values, df['Lower'].tail(1).values, df['MA'].tail(1).values,
              df['Upper'].tail(1).values, df['Close'].tail(1).values, df['MACD'].tail(1).values, df['Signal_Line'].tail(1).values)
        LastTI = time.time()
