import csv
import time
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import shioaji as sj
from collections import defaultdict, deque
from shioaji import TickFOPv1, Exchange
from threading import Event

minute_close = pd.Series()
stock = 0
token = '4cwTgoUM0Npnnob1D0aUHCYWxN6huiqVF9poI0G1Efe'

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

today = time.strftime('%y_%m_%d', time.localtime())
pathtoday = str(r'C:\_Phil\Private\stockprice\Price_Log' + today + '.csv')
# with open(pathtoday, 'a+', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Time', 'open', 'underlying', 'bid_side_total_vol',
#                      'ask_side_total_vol', 'avg_price', 'close', 'high',
#                      'low', 'amount', 'total_amount', 'volume', 'total_volume',
#                      'tick_type', 'chg_type', 'price_chg', 'pct_chg', 'simtrade'])
api = sj.Shioaji(simulation=True) # 模擬模式
api.login(api_key="H6WLFjAN6QaRKucnGBm9TgEGpghBNNhafRyj3xjMLp7M",
          secret_key="HRgYZfKx7fz2BFYgxxcdxWvtXpCMYPj6BgsqySArEdmF",
          fetch_contract=False)

api.fetch_contracts(contract_download=True)
# subscribe
api.quote.subscribe(
    api.Contracts.Futures.MXF['MXF202307'],
    quote_type = sj.constant.QuoteType.Tick,
    version = sj.constant.QuoteVersion.v1
)
# set context
msg_queue = defaultdict(deque)
api.set_context(msg_queue)
# In order to use context, set bind=True
@api.on_tick_fop_v1(bind=True)
def quote_callback(self, exchange:Exchange, tick: TickFOPv1):
    #print(tick)
    price = tick.amount
    volume = tick.volume
    price_chg = tick.price_chg
    print(Exchange, price, volume, price_chg)


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


Event().wait()
contracts = [api.Contracts.Futures['MXF202307']]

for i in range(0, 12):
    snapshots = api.snapshots(contracts)
    minute_close = minute_close.append(pd.Series(
        [snapshots[0].close],
        index=[pd.to_datetime(snapshots[0].ts, unit='ns')]
    ))
    time.sleep(60)

# 開始算RSI
for i in range(0, 700):
    # 抓snapshot
    snapshots = api.snapshots(contracts)

    # 存到分k收盤價的series
    minute_close = minute_close.append(pd.Series(
        [snapshots[0].close],
        index=[pd.to_datetime(snapshots[0].ts, unit='ns')]
    ))

    # 計算rsi
    rsi = RSI(minute_close)

    # 觸發訊號判斷
    if rsi <= 30 and rsi >= 0 and stock == 0:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time, "BUY AT ", snapshots[0].close)
        message = '%s%s%s%s'% ("Current Time =", current_time, "BUY AT ", snapshots[0].close)
        lineNotifyMessage(token, message)
        stock += 1
    if rsi >= 70 and stock == 1:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time, "SELL AT ", snapshots[0].close)
        message = '%s%s%s%s' % ("Current Time =", current_time, "SELL AT ", snapshots[0].close)
        lineNotifyMessage(token, message)
        stock -= 1
    time.sleep(60)

# time.sleep(5)
# while True:
#     pass
    # datetime = tick.datetime
    # Popen = tick.open
    # underlying_price = tick.underlying_price
    # bid_side_total_vol = tick.bid_side_total_vol
    # ask_side_total_vol = tick.ask_side_total_vol
    # avg_price = tick.avg_price
    # close = tick.close
    # high = tick.high
    # low = tick.low
    # amount = tick.amount
    # total_amount = tick.total_amount
    # volume = tick.volume
    # total_volume = tick.total_volume
    # tick_type = tick.tick_type
    # chg_type = tick.chg_type
    # price_chg = tick.price_chg
    # pct_chg = tick.pct_chg
    # simtrade = tick.simtrade
    # print(amount)
    # with open(pathtoday, 'a+', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(datetime, Popen, underlying_price, bid_side_total_vol,
    #                     ask_side_total_vol, avg_price, close, high,
    #                     low, amount, total_amount, volume, total_volume,
    #                     tick_type, chg_type, price_chg, pct_chg, simtrade)