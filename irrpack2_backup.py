import time
import json
import crcmod
import serial
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime

with open(r'D:\pythonINI\offset.txt') as init:
    offset1 = init.readline()
    offset1 = offset1.strip('\n')
    offset2 = init.readline()
    offset2 = offset2.strip('\n')

today = time.strftime('%y_%m_%d', time.localtime())
pathtoday = str(today + '.txt')

cmdMeter1offset = [0x01, 0x06, 0x00, 0x04, 0x00, 0x00, 0xC8, 0x0B]
cmdMeter2offset = [0x02, 0x06, 0x00, 0x04, 0x00, 0x00, 0xC8, 0x38]
cmd7015TP1 = [0x23, 0x30, 0x31, 0x30, 0x0D]
cmd7015TP2 = [0x23, 0x30, 0x31, 0x31, 0x0D]
T1 = 0
T2 = 0
irr1 = 0
# hexirr1 = hex(irr1)[2:].zfill(4)
irr2 = 0
# hexirr2 = hex(irr2)[2:].zfill(4)
serCOM7 = serial.Serial()
serCOM7.port = "COM7"
serCOM7.baudrate = 9600
serCOM7.bytesize = serial.EIGHTBITS
serCOM7.parity = serial.PARITY_NONE
serCOM7.stopbits = serial.STOPBITS_ONE
serCOM7.timeout = 0.5
serCOM7.writeTimeout = 0.5
serCOM7.xonxoff = False
serCOM7.rtscts = False
serCOM7.dsrdtr = False
serCOM7.open()

serCOM2 = serial.Serial()
serCOM2.port = "COM2"
serCOM2.baudrate = 9600
serCOM2.bytesize = serial.EIGHTBITS
serCOM2.parity = serial.PARITY_NONE
serCOM2.stopbits = serial.STOPBITS_ONE
serCOM2.timeout = 0.5
serCOM2.writeTimeout = 0.5
serCOM2.xonxoff = False
serCOM2.rtscts = False
serCOM2.dsrdtr = False
serCOM2.open()

serCOM1 = serial.Serial()
serCOM1.port = "COM1"
serCOM1.baudrate = 9600
serCOM1.bytesize = serial.EIGHTBITS
serCOM1.parity = serial.PARITY_NONE
serCOM1.stopbits = serial.STOPBITS_ONE
serCOM1.timeout = 0.5
serCOM1.writeTimeout = 0.5
serCOM1.xonxoff = False
serCOM1.rtscts = False
serCOM1.dsrdtr = False
serCOM1.open()

serCOM1.write(cmdMeter1offset)
time.sleep(0.1)
serCOM1.write(cmdMeter2offset)
time.sleep(0.1)


def sendDCONT1(command):
    try:
        serCOM2.write(command)
        response = serCOM2.readline().decode('ascii').strip()
        TempTP1 = response[3:9]
        labelTP1.config(text=f"TP1: {TempTP1}")
        return TempTP1
    except Exception as e:
        labelErrorCode.config(text=f"ErrorCode:TP1 Error")
        print('TP1 Error')


def sendDCONT2(command):
    try:
        serCOM2.write(command)
        response = serCOM2.readline().decode('ascii').strip()
        TempTP2 = response[3:9]
        labelTP2.config(text=f"TP2: {TempTP2}")
        return TempTP2
    except Exception as e:
        labelErrorCode.config(text=f"ErrorCode:TP2 Error")
        print('TP2 Error')


def calculate_crc16(data):
    crc16_func = crcmod.predefined.Crc('modbus')
    crc16_func.update(data)
    return crc16_func.crcValue


def read_serial():
    try:
        global T1, T2, irr1, irr2, TP1, TP2
        if serCOM7.inWaiting() > 0:
            data = serCOM7.readline()
            jsondata = json.loads(data)
            T1 = jsondata["T1"]
            T2 = jsondata["T2"]
            ORIirr1 = jsondata["irr1"]
            ORIirr2 = jsondata["irr2"]
            SETirr1 = int(ORIirr1 * float(offset1))
            SETirr2 = int(ORIirr2 * float(offset2))
            time.sleep(0.1)
            labelT1.config(text=f"miniT1: {T1}")
            labelT2.config(text=f"miniT2: {T2}")
            labelirr1.config(text=f"irr1: {SETirr1}")
            labelirr2.config(text=f"irr2: {SETirr2}")
            labelORIirr1.config(text=f"irr1Cur: {ORIirr1}")
            labelORIirr2.config(text=f"irr2Cur: {ORIirr2}")
            labelTime.config(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            Meter1send(SETirr1)
            Meter2send(SETirr2)
        root.after(10, read_serial)
    except Exception as e:
        labelErrorCode.config(text=f"ErrorCode:raspberry Error")
        print('raspberry Error')


def Meter1send(irr1):
    try:
        irr1bytes = irr1.to_bytes(2, byteorder='big')
        cmdMeter1 = bytes.fromhex('01060000') + irr1bytes
        crc16_value1 = calculate_crc16(cmdMeter1)
        crc16_bytes1 = bytes([(crc16_value1) & 0xFF, (crc16_value1 >> 8) & 0xFF])
        cmd_with_crc1 = cmdMeter1 + crc16_bytes1
        serCOM1.write(cmd_with_crc1)
    except Exception as e:
        labelErrorCode.config(text=f"ErrorCode:Meter1 Error")
        print('Meter1 Error')


def Meter2send(irr2):
    try:
        irr2bytes = irr2.to_bytes(2, byteorder='big')
        cmdMeter2 = bytes.fromhex('02060000') + irr2bytes
        crc16_value2 = calculate_crc16(cmdMeter2)
        crc16_bytes2 = bytes([(crc16_value2) & 0xFF, (crc16_value2 >> 8) & 0xFF])
        cmd_with_crc2 = cmdMeter2 + crc16_bytes2
        serCOM1.write(cmd_with_crc2)
    except Exception as e:
        labelErrorCode.config(text=f"ErrorCode:Meter2 Error")
        print('Meter2 Error')


# def csv_saving():
#    nowtime = time.strftime('%H:%M:%S', time.localtime())
#    with open(pathtoday, 'a+', newline='') as file:

root = ttk.Window(title='Irrpack2')
# root.title("Irr pack 2")
root.geometry("1024x768")
style = ttk.Style(theme='solar')
labelirr1 = ttk.Label(root, text='irr1:')
labelirr1.config(font=("思源黑體", 30))
labelirr1.place(x=100, y=100)
labelirr2 = ttk.Label(root, text="irr2:")
labelirr2.config(font=("思源黑體", 30))
labelirr2.place(x=100, y=150)
labelTP1 = ttk.Label(root, text="TP1:")
labelTP1.config(font=("思源黑體", 30))
labelTP1.place(x=100, y=200)
labelTP2 = ttk.Label(root, text="TP2:")
labelTP2.config(font=("思源黑體", 30))
labelTP2.place(x=100, y=250)
labelT1 = ttk.Label(root, text="miniT1:")
labelT1.config(font=("思源黑體", 20))
labelT1.place(x=100, y=400)
labelT2 = ttk.Label(root, text="miniT2:")
labelT2.config(font=("思源黑體", 20))
labelT2.place(x=100, y=450)
labelORIirr1 = ttk.Label(root, text="oriirr1:")
labelORIirr1.config(font=("思源黑體", 20))
labelORIirr1.place(x=100, y=500)
labelORIirr2 = ttk.Label(root, text="oriirr2:")
labelORIirr2.config(font=("思源黑體", 20))
labelORIirr2.place(x=100, y=550)
labelTime = ttk.Label(root, text="Time:")
labelTime.config(font=("思源黑體", 40))
labelTime.place(x=250, y=10)
labelTime.config(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
labelErrorCode = ttk.Label(root, text="ErrorCode:")
labelErrorCode.config(font=("思源黑體", 20))
labelErrorCode.place(x=450, y=500)
read_serial()
TP1 = sendDCONT1(cmd7015TP1)
TP2 = sendDCONT2(cmd7015TP2)
time.sleep(0.001)
root.mainloop()










