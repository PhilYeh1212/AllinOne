import shioaji as sj
import pandas as pd
import numpy as np
import talib
import requests
import time
import csv
from datetime import datetime, date, timedelta
from shioaji import TickFOPv1, Exchange

startdate = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
print(startdate)
minute_close = pd.Series()
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
#print(api.Contracts)
contracts = [api.Contracts.Futures.MXF['MXF202307']]
today = time.strftime('%Y-%m-%d')
#print(today)
symbol = "TXFF"  # 台指期代號
enddate = today  # 結束日期

def quote_callback(exchange:Exchange, tick:TickFOPv1):
    print(f"Exchange: {exchange}, Tick: {tick}")

kbars = api.kbars(
    contract=api.Contracts.Futures.MXF['MXF202307'],
    start=startdate, end=enddate
)
LastTI = 0

while True:
    inTI = time.time()
    #for i in range(0, 12):
    if inTI - LastTI >= 60:
        # 將Tick數據轉換為DataFrame
        df = pd.DataFrame({**kbars})
        df.ts = pd.to_datetime(df.ts)
        df.head(5)
        # 計算布林通道指標
        df['MA'] = talib.SMA(df['Close'])  # 計算20日移動平均線
        df['STD'] = talib.STDDEV(df['Close'], timeperiod=20)  # 計算20日收盤價的標準差
        df['Upper'] = df['MA'] + 2 * df['STD']  # 計算布林通道上軌
        df['Lower'] = df['MA'] - 2 * df['STD']  # 計算布林通道下軌

        # 計算隨機指標
        df['K'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=14)[0]  # 計算K值
        df['D'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=14)[1]  # 計算D值

        # 設置交易策略
        # 執行交易
        # signal = row['Signal']
        # close = row['Close']
        #print(signal, close)
        if signal == 1 and Buystock == 0:  # 買入訊號且無持倉
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "B ", close)
            message = '%s %s %s' % (current_time, "B ", close)
            lineNotifyMessage(token, message)
            # order = api.insert_order(
            #     symbol=symbol,
            #     price=close,
            #     action=sj.constant.Action.Buy,
            #     price_type=sj.constant.TFTOrderPriceType.LMT,
            #     order_type=sj.constant.TFTOrderType.ROD,
            #     quantity=1,
            # )
            # positions.append(order)
        elif signal == -1 and positions:  # 賣出訊號且有持倉
            now = datetime.now()
            current_time = now.strftime("%y%m%d %H:%M:%S")
            print("Current Time =", current_time, "S ", close)
            message = '%s %s %s' % (current_time, "S ", close)
            lineNotifyMessage(token, message)
            # order = api.insert_order(
            #     symbol=symbol,
            #     price=close,
            #     action=sj.constant.Action.Sell,
            #     price_type=sj.constant.TFTOrderPriceType.LMT,
            #     order_type=sj.constant.TFTOrderType.ROD,
            #     quantity=1,
            # )
            # api.update_status([order])