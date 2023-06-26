import csv
import time
import shioaji as sj
from collections import defaultdict, deque
from shioaji import TickFOPv1, Exchange

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

# set context
msg_queue = defaultdict(deque)
api.set_context(msg_queue)
# In order to use context, set bind=True
@api.on_tick_fop_v1(bind=True)
def quote_callback(self, exchange:Exchange, tick: TickFOPv1):
    price = tick.close
    volume = tick.volume
    print(Exchange, price, volume)
api.fetch_contracts(contract_download=True)
# subscribe
api.quote.subscribe(
    api.Contracts.Futures.MXF['MXF202306'],
    quote_type = sj.constant.QuoteType.Tick,
    version = sj.constant.QuoteVersion.v1
)

kbars = api.kbars(
    contract=api.Contracts.Futures.MXF.MXF202306,
    start="2023-06-20",
    end="2023-06-20",
)
kbars


time.sleep(5)
while True:
    pass
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