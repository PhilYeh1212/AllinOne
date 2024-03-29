import os
import time
import json
import math
import binascii
import machine
import ustruct as struct

# 設定 UART1
USB = machine.UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=machine.Pin(0), rx=machine.Pin(1))
uart = machine.UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=machine.Pin(4), rx=machine.Pin(5))

# Modbus RTU 命令
READ_HOLDING_REGISTERS = 0x03
Temp1 = machine.ADC(26)
Temp2 = machine.ADC(27)
beta_value = 3950.0
r0 = 10000.0
lastTi = 0


# 函數：計算 CRC16 校驗碼
def crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)


# 函數：發送 Modbus RTU 命令
def send_modbus_command(slave_address, function_code, starting_address, quantity):
    # 組合 Modbus RTU 命令
    command = struct.pack('>BBHH', slave_address, function_code, starting_address, quantity)
    command += crc16(command)

    # 發送命令
    # print(binascii.hexlify(command).decode())
    uart.write(command)


# 函數：讀取 Modbus RTU 命令的回應
def read_modbus_response(expected_length):
    response = uart.read(expected_length)
    return response


def read_temperature():
    T2 = Temp1.read_u16()
    T1 = Temp2.read_u16()
    voltage = (T1 / 65535.0) * 3.3

    r1 = r0 / ((3.3 / voltage) - 1.0)

    temperature1 = (1.0 / ((math.log(r1 / r0) / beta_value) + (1.0 / 298.15))) - 273.15

    voltage = (T2 / 65535.0) * 3.3

    r2 = r0 / ((3.3 / voltage) - 1.0)

    temperature2 = (1.0 / ((math.log(r2 / r0) / beta_value) + (1.0 / 298.15))) - 273.15

    return temperature1, temperature2


# 主程式
def GetIrr1():
    slave1_address = 0x01
    starting_address = 0x0002
    quantity = 2
    # 發送讀取保持寄存器命令
    send_modbus_command(slave1_address, READ_HOLDING_REGISTERS, starting_address, quantity)
    # 等待並讀取回應
    response = read_modbus_response(5 + 2 * quantity)  # 回應包含 5 個固定位元組和每個保持寄存器 2 個位元組

    # 解析回應
    if response:
        try:
            slave1_address, function_code, byte_count = struct.unpack('>BBB', response[:3])
            data = response[3:-2]
            crc_received = struct.unpack('<H', response[-2:])[0]

            # 驗證 CRC16 校驗碼
            crc_calculated = struct.unpack('<H', crc16(response[:-2]))[0]
            if crc_received == crc_calculated:
                # 處理回應資料
                # print(binascii.hexlify(data).decode())
                irr1 = data[3] + (data[2] << 8)
                return irr1
            else:
                print("CRC16 Check Failed")
        except Exception as e:
            print(e)
    else:
        print("module1 No Response")
        irr1 = 0
        return irr1


def GetIrr2():
    slave2_address = 0x02
    starting_address = 0x0002
    quantity = 2
    # 發送讀取保持寄存器命令
    send_modbus_command(slave2_address, READ_HOLDING_REGISTERS, starting_address, quantity)
    # 等待並讀取回應
    response = read_modbus_response(5 + 2 * quantity)  # 回應包含 5 個固定位元組和每個保持寄存器 2 個位元組

    # 解析回應
    if response:
        try:
            slave2_address, function_code, byte_count = struct.unpack('>BBB', response[:3])
            data = response[3:-2]
            crc_received = struct.unpack('<H', response[-2:])[0]

            # 驗證 CRC16 校驗碼
            crc_calculated = struct.unpack('<H', crc16(response[:-2]))[0]
            if crc_received == crc_calculated:
                # 處理回應資料
                # print(binascii.hexlify(data).decode())
                irr2 = data[3] + (data[2] << 8)
                # print('IRR2', irr2)
                return irr2
            else:
                print("CRC16 Check Failed")
        except Exception as e:
            print(e)
    else:
        print("module2 No Response")
        irr2 = 0
        return irr2


# 執行主程式

while True:
    inTi = time.time()
    irr1 = GetIrr1()
    time.sleep(0.05)
    irr2 = GetIrr2()
    time.sleep(1)
    temp1, temp2 = read_temperature()
    if inTi - lastTi >= 9:
        try:
            data = json.dumps({'irr1': irr1, 'irr2': irr2, 'T1': temp1, 'T2': temp2})
            print(data)
            lastTi = time.time()
        except Exception as e:
            print(e)
            lastTi = time.time()


