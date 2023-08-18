import os
import csv
import time
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import shioaji as sj
from shioaji import TickFOPv1, Exchange
import shioaji

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
contracts = [api.Contracts.Futures.MXF['MXF202307']]

# def quote_callback(self, exchange:Exchange, tick: TickFOPv1):
#     #print(tick)
#     price = tick.amount
#     volume = tick.volume
#     price_chg = tick.price_chg
#     # print(Exchange, price, volume, price_chg)
#
# # subscribe
# api.quote.subscribe(
#     api.Contracts.Futures.MXF['MXF202307'],
#     quote_type = sj.constant.QuoteType.Tick,
#     version = sj.constant.QuoteVersion.v1
# )
# # set


def RSI(close, period=12):
    # 整理資料
    Close = close[-13:]
    Chg = Close - Close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg > 0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg < 0])
    Chg_neg = Chg_neg.fillna(0)

    # 計算平均漲跌幅度
    up_mean = np.mean(Chg_pos.values[-12:])
    down_mean = np.mean(Chg_neg.values[-12:])

    # 計算 RSI
    if (up_mean + down_mean > 0):
        rsi = 100 * up_mean / (up_mean + down_mean)
    else:
        rsi = -1

    return rsi


LastTI = 0
mainTI = time.time() + 720

while True:
    inTI = time.time()

    #for i in range(0, 12):
    if inTI - LastTI >= 60 and Openner <= 11:
        snapshots = api.snapshots(contracts)
        minute_close = minute_close._append(pd.Series([snapshots[0].close],
                                                      index=[pd.to_datetime(snapshots[0].ts, unit='ns')]))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), minute_close)
        LastTI = time.time()
        Openner += 1
    # 開始算RSI
    if inTI - mainTI >= 60:
    #for i in range(0, 400):
        # 抓snapshot
        snapshots = api.snapshots(contracts)

        # 存到分k收盤價的series
        minute_close = minute_close._append(pd.Series(
            [snapshots[0].close],
            index=[pd.to_datetime(snapshots[0].ts, unit='ns')]
        ))
        # 計算rsi
        rsi = RSI(minute_close)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), rsi, snapshots[0].close)

        if Buystock == 0 and Sellstock == 0:
            if 30 >= rsi >= 0:
                buyD = 1
            if rsi >= 30 and buyD == 1:
                buyU = 2
            if buyU == 2:
                try:
                    now = datetime.now()
                    current_time = now.strftime("%y%m%d %H:%M:%S")
                    print("Current Time =", current_time, "B ", snapshots[0].close)
                    Buypoint = snapshots[0].close
                    # order = api.Order(
                    #     action=sj.constant.Action.Buy,
                    #     price=snapshots[0].close,
                    #     quantity=2,
                    #     price_type="LMT",
                    #     order_type="ROD",
                    #     octype="Auto",
                    #     account=api.futopt_account
                    # )
                    # trade = api.place_order(contracts, order)
                    # print(trade)
                    message = '%s %s%s %s' % (current_time, "B ", snapshots[0].close)
                    lineNotifyMessage(token, message)
                    Buystock += 1
                    buyU = 0
                    buyD = 0
                except:
                    print('Buy Error Retry')
        if Sellstock == 0 and Buystock == 0:
            if rsi >= 70:
                SellU = 1
            if rsi <= 70 and SellU == 1:
                SellD = 2
            if SellD == 2:
                try:
                    now = datetime.now()
                    current_time = now.strftime("%y%m%d %H:%M:%S")
                    print("Current Time =", current_time, "S ", snapshots[0].close)
                    Sellpoint = snapshots[0].close
                    # order = api.Order(
                    #     action=sj.constant.Action.Sell,
                    #     price=snapshots[0].close,
                    #     quantity=2,
                    #     price_type="LMT",
                    #     order_type="ROD",
                    #     octype="Auto",
                    #     account=api.futopt_account
                    # )
                    # trade = api.place_order(contracts, order)
                    # print(trade)
                    message = '%s %s%s %s' % (current_time, "S ", snapshots[0].close)
                    lineNotifyMessage(token, message)
                    Sellstock += 1
                    SellU = 0
                    SellD = 0
                except:
                    print('Sell Error Retry')
        if Buystock == 1:
            # if abs(Buypoint - snapshots[0].close) >= 30:
            #     diff = abs(snapshots[0].close - Buypoint)
            #     earn = -(diff * 50)
            #     message = '停損出場'
            #     lineNotifyMessage(token, message)
            #     Buystock -= 1
            if rsi >= 70:
                SellUs = 1
            if rsi <= 70 and SellUs == 1:
                SellDs = 2
            if SellDs == 2:
                now = datetime.now()
                current_time = now.strftime("%y%m%d %H:%M:%S")
                print("Current Time =", current_time, "S ", snapshots[0].close)
                Sellpoint = snapshots[0].close
                # order = api.Order(
                #     action=sj.constant.Action.Sell,
                #     price=snapshots[0].close,
                #     quantity=2,
                #     price_type="LMT",
                #     order_type="ROD",
                #     octype="Cover",
                #     account=api.futopt_account
                # )
                # trade = api.place_order(contracts, order)
                # print(trade)
                diff = Sellpoint - Buypoint
                earn = diff * 50
                message = '%s %s%s %s,%s,%s' % (current_time, "S ", snapshots[0].close, earn)
                lineNotifyMessage(token, message)
                with open(pathtoday, 'a+', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([current_time, Buypoint, Sellpoint, diff, earn])
                Buystock -= 1
                SellUs = 0
                SellDs = 0
        if Sellstock == 1:
            # Sell 觸發訊號判斷
            # if abs(Sellpoint - snapshots[0].close) >= 30:
            #     diff = abs(snapshots[0].close - Buypoint)
            #     earn = -(diff * 50)
            #     print(diff)
            #     message = '停損出場'
            #     lineNotifyMessage(token, message)
            #     Sellstock -= 1
            if 30 >= rsi >= 0:
                buyDs = 1
            if rsi >= 30 and buyDs == 1:
                buyUs = 2
            if buyUs == 2:
                now = datetime.now()
                current_time = now.strftime("%y%m%d %H:%M:%S")
                print("Current Time =", current_time, "B ", snapshots[0].close)
                Buypoint = snapshots[0].close
                # order = api.Order(
                #     action=sj.constant.Action.Buy,
                #     price=snapshots[0].close,
                #     quantity=2,
                #     price_type="LMT",
                #     order_type="ROD",
                #     octype="Cover",
                #     account=api.futopt_account
                # )
                # trade = api.place_order(contracts, order)
                # print(trade)
                message = '%s %s%s %s,%s,%s' % (current_time, "B ", snapshots[0].close, earn)
                lineNotifyMessage(token, message)
                diff = Sellpoint - Buypoint
                earn = diff * 50
                print(diff)


                Sellstock -= 1
                buyDs = 0
                buyUs = 0
        mainTI = time.time()