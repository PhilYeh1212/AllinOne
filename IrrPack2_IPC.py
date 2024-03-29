import os
import csv
import time
import json
import crcmod
import serial
import random
import tkinter as tk
import ttkbootstrap as ttk
# import paho.mqtt.client as mqtt
from ttkbootstrap.constants import *
from datetime import datetime

with open(r'D:\pythonINI\offset.txt') as init:
    offset1 = init.readline()
    offset1 = float(offset1.strip('\n'))
    offset2 = init.readline()
    offset2 = float(offset2.strip('\n'))

today = time.strftime('%y_%m_%d', time.localtime())
pathtoday = '%s\%s.%s' % (r'C:\DDS data', today, 'csv')

cmdMeter1offset = [0x01, 0x06, 0x00, 0x04, 0x00, 0x00, 0xC8, 0x0B]
cmdMeter2offset = [0x02, 0x06, 0x00, 0x04, 0x00, 0x00, 0xC8, 0x38]
cmd7015TP1 = [0x23, 0x30, 0x31, 0x30, 0x0D]
cmd7015TP2 = [0x23, 0x30, 0x31, 0x31, 0x0D]
irrcmd = [0x02]
irrstart = [0x69, 0x6D, 0x70, 0x6F, 0x72, 0x74, 0x20, 0x6D, 0x61, 0x69, 0x6E, 0x2E, 0x70, 0x79, 0x0D]

serCOM7 = serial.Serial(port="COM7", baudrate=9600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                        timeout=0.1, writeTimeout=0.1, xonxoff=False, rtscts=False, dsrdtr=False)
serCOM2 = serial.Serial(port="COM2", baudrate=9600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                        timeout=0.1, writeTimeout=0.1, xonxoff=False, rtscts=False, dsrdtr=False)
serCOM1 = serial.Serial(port="COM1", baudrate=9600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                        timeout=0.1, writeTimeout=0.1, xonxoff=False, rtscts=False, dsrdtr=False)

serCOM1.write(cmdMeter1offset)
time.sleep(0.1)
serCOM1.write(cmdMeter2offset)
time.sleep(0.1)
# client_id = f'publish-{random.randint(0,1000)}'
root = ttk.Window(title='Irrpack2')
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


# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.username_pw_set("extel","oerlikon")
# client.connect("35.221.195.52", 8883, 60)


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
    #      try:
    global T1, T2, irr1, irr2, TP1, TP2
    if serCOM7.inWaiting() > 0:
        data = serCOM7.readline()
        print(data)
        jsondata = json.loads(data)
        T1 = float(jsondata["T1"])
        T2 = float(jsondata["T2"])
        ORIirr1 = float(jsondata["irr1"])
        ORIirr2 = float(jsondata["irr2"])
        SETirr1 = (ORIirr1 * 1000 * (1 - 0.0005 * (T1 - 25)) / offset1) / 1000
        SETirr2 = (ORIirr2 * 1000 * (1 - 0.0005 * (T2 - 25)) / offset2) / 1000
        SETirr1met = float(SETirr1)
        SETirr2met = float(SETirr2)
        time.sleep(0.1)
        labelT1.config(text=f"miniT1: {T1}")
        labelT2.config(text=f"miniT2: {T2}")
        labelirr1.config(text=f"irr1: {SETirr1}")
        labelirr2.config(text=f"irr2: {SETirr2}")
        labelORIirr1.config(text=f"irr1Cur: {ORIirr1}")
        labelORIirr2.config(text=f"irr2Cur: {ORIirr2}")
        labelTime.config(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        Meter1send(int(SETirr1met))
        Meter2send(int(SETirr2met))
        TP1 = sendDCONT1(cmd7015TP1)
        TP2 = sendDCONT2(cmd7015TP2)
        # payload = {'IRR1':SETirr1, 'IRR2':SETirr2, 'TP1':TP1, 'TP2':TP2}
        # client.publish("extel/irrpack2", json.dumps(payload))
        csv_saving(SETirr1, SETirr2, ORIirr1, ORIirr2, TP1, TP2, T1, T2)
    root.after(10, read_serial)


#      except Exception as e:
#          labelErrorCode.config(text=f"ErrorCode:raspberry Error")
#          print('raspberry Error')

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


def csv_saving(irr1, irr2, irr1Cur, irr2Cur, TP1, TP2, T1, T2):
    if os.path.isfile(pathtoday):
        pass
    else:
        with open(pathtoday, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'IRR_a', 'IRR_b', 'PVTemp_a', 'PVTemp_b',
                             'mCur_a', 'mCur_b', 'mTemp_a', 'mTemp_b'])

    nowtime = time.strftime('%H:%M:%S', time.localtime())
    with open(pathtoday, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([nowtime, irr1, irr2, TP1, TP2, irr1Cur, irr2Cur, T1, T2])


time.sleep(0.01)
serCOM7.write(irrcmd)
time.sleep(0.01)
serCOM7.write(irrstart)

while True:
    read_serial()
    root.mainloop()
    time.sleep(0.001)








