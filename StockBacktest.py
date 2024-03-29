import pandas as pd
import numpy as np
import talib


futures_data = pd.read_csv('TXF2.csv')
futures_data['Date'] = pd.to_datetime(futures_data['Date'])
futures_data.set_index('Date', inplace=True)
position = 0
# 2. 计算MACD和KDJ指标
def calculate_technical_indicators(data):
    short_window = 12
    long_window = 26
    signal_window = 12
    stoch_period = 0

    data['MACD'], data['Signal_Line'], _ = talib.MACD(data['Close'], fastperiod=short_window, slowperiod=long_window,
                                                      signalperiod=signal_window)
    data['MA'] = talib.SMA(data['Close'], timeperiod=18)
    data['STD'] = talib.STDDEV(data['Close'], timeperiod=18)
    data['Upper'] = data['MA'] + 2 * data['STD']
    data['Lower'] = data['MA'] - 2.1 * data['STD']


    fastk_period = 5
    slowk_period = 3
    slowd_period = 3

    data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Close'],
                                               fastk_period=fastk_period, slowk_period=slowk_period,
                                               slowd_period=slowd_period)

    data['J'] = 3 * data['K'] - 2 * data['D']

def implement_strategy(data):
    global position
    data['Position'] = np.where((data['MACD'] > data['Signal_Line']) & (data['J'] > 0) & (position == 0) & (data['Close'] < data['MA']) & (data['K'] > data['D']), 1, 0)
    data['Position'] = np.where((data['MACD'] < data['Signal_Line']) & (data['J'] <= 0) & (data['Close'] < data['MA']) & (data['K'] < data['D']), -1, data['Position'])

def backtest_strategy(data):
    global position
    # starting_balance = 100000
    # balance = starting_balance
    # position = 0
    #
    # for index, row in data.iterrows():
    #     if row['Position'] == 1 and position == 0:
    #
    #         position = balance / row['Close']
    #         print(position, balance, row['Close'])
    #         balance = 0
    #     elif row['Position'] == -1 and position > 0:
    #
    #         balance = position * row['Close']
    #         print(position, balance, row['Close'])
    #         position = 0
    initial_balance = 50000
    buy_stock = 0
    balance = initial_balance
    position = 0
    buy_price = 50000
    for i in range(1, len(data)):
        if data['Position'][i] == 1 and position == 0:
            position = 1
            buy_stock = data['Close'][i]
            print('1', position, buy_stock, data['Close'][i], balance)
        elif data['Position'][i] == -1 and position > 0:
            balance = balance + (position * (data['Close'][i] - buy_stock)) * 50
            print('2', position, buy_stock, data['Close'][i], balance)
            position = 0
        if (buy_stock - data['Close'][i]) >= 10:
            balance = balance + (position * (data['Close'][i] - buy_stock)) * 50
            print('3', position, buy_stock, data['Close'][i], balance)
            position = 0
        else:
            pass

    final_balance = balance + (position * data['Close'].iloc[-1])
    #print(position, data['Close'].iloc[-1])
    return final_balance



if __name__ == "__main__":

    data = pd.read_csv('TXF.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)


    calculate_technical_indicators(data)


    implement_strategy(data)


    final_value = backtest_strategy(data)
    print("Final Portfolio Value: $", final_value)