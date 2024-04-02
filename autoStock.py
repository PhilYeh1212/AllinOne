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
buyU = 0
CheckPointB = 0
CheckPointD = 0
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
print(api.Contracts.Futures.MXF)
contracts = [api.Contracts.Futures.MXF.MXFR1]
today = time.strftime('%Y-%m-%d')
# print(today)
#symbol = "TXFF"
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
    if inTI - LastTI >= 1:
        # for i in range(0, 12):
        # price = dftick['amount'].tail(1).values/dftick['volume'].tail(1).values
        # print(price)
        snapshots = api.snapshots(contracts)
        kbars = api.kbars(
            contract=api.Contracts.Futures.MXF.MXFR1,
            start=startdate, end=enddate
        )
        # 將Tick數據轉換為DataFrame
        df = pd.DataFrame({**kbars})
        df.ts = pd.to_datetime(df.ts)
        df.head(20)
        df['rsi'] = talib.RSI(df['Close'], timeperiod=14)
        lastRSI = df['rsi'].tail(1).values[-1]
        if (lastRSI < 20.0):
            if (lastRSI > 20.0):
                buyU = 1
            else:
                buyU = 0
        else:
            buyU = 0

        if (lastRSI > 80.0):
            if (lastRSI < 80.0):
                sellD = 1
            else:
                sellD = 0
        else:
            sellD = 0

        if buyU == 1 and Buystock == 0:
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "B ")
            BuyPoint = snapshots[0].close
            CheckPointB = snapshots[0].close
            Buystock += 1
            buyU == 1
            message = '%s %s %s' % (current_time, "B ", BuyPoint)
            lineNotifyMessage(token, message)
        elif sellD == 1 and Buystock == 0:
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "S ")
            SellPoint = snapshots[0].close
            CheckPointD = snapshots[0].close
            message = '%s %s %s' % (current_time, "S ", SellPoint)
            lineNotifyMessage(token, message)
            Buystock += 1
            sellD == 1

        if (buyU == 1 and Buystock != 0 and (snapshots[0].close - CheckPointB) >= 5):
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "B ")
            CheckPointB = snapshots[0].close
            Buystock += 1
            message = '%s %s %s' % (current_time, "B ", BuyPoint, CheckPointB)
            lineNotifyMessage(token, message)
            buyU = 1
        elif (buyU == 1 and Buystock > 0 and (CheckPointB - snapshots[0].close) > 0 and (CheckPointB - snapshots[0].close) < 5):
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "S ")
            earn = (snapshots[0].close - CheckPointB) * 50
            message = '%s %s %s' % (current_time, "S ", snapshots[0].close, earn)
            buyU = 0
            lineNotifyMessage(token, message)
            Buystock = 0
        if (sellD == 1 and Buystock != 0 and (CheckPointD - snapshots[0].close) > 5):
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "S ")
            CheckPointD = snapshots[0].close
            message = '%s %s %s' % (current_time, "S ", SellPoint, CheckPointD)
            lineNotifyMessage(token, message)
            Buystock += 1
            sellD == 1
        elif (sellD == 1 and Buystock > 0 and (snapshots[0].close - CheckPointD) > 0 and (snapshots[0].close - CheckPointD) > 5):
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "B ")
            earn = (CheckPointD - snapshots[0].close) * 50
            message = '%s %s %s' % (current_time, "B ", snapshots[0].close)
            lineNotifyMessage(token, message)
            Buystock = 0
            sellD = 0

        print(df['rsi'].tail(1).values, snapshots[0].close)
        LastTI = time.time()

#order範例
# order = api.insert_order(
            #     symbol=symbol,
            #     price=close,
            #     action=sj.constant.Action.Buy,
            #     price_type=sj.constant.TFTOrderPriceType.LMT,
            #     order_type=sj.constant.TFTOrderType.ROD,
            #     quantity=1,
            # )
            # positions.append(order)

