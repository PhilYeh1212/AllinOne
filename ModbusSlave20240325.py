import os
import csv
import time
import math
import serial
import mysql.connector

today = time.strftime('%y_%m_%d', time.localtime())
file = str(today + '_Soiling-data.txt')
path = '%s\%s' % (r"C:\soft\soiling", file)
lastTi = 0


def calc_crc(string):
    data = bytearray.fromhex(string)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    result = hex(((crc & 0xff) << 8) + (crc >> 8))
    result = result[2:]  # 去掉 '0x' 前綴
    result = result.zfill(4)  # 在前面補齊 0，確保長度為 4
    return result


try:
    mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306,
                                   database="vena_dds_global")
    offsetini = open(r'C:\DDS Data\offset.ini', 'r')
    Line1 = offsetini.readlines()
    dasID = Line1[9].split(':')
    dasID = dasID[1].replace('\n', '')
    offsetini.close

    SQL = '%s%s%s' % ("SELECT date, soiling FROM ", dasID, ".Daily_soiling order by date desc limit 1")
    cursor = mydb.cursor()
    cursor.execute(SQL)
    data = cursor.fetchall()
    soiling = '%04d' % (math.floor(data[0][1] * 1000))
    with open(path, 'a+') as csvfile:
        csvfile.write(today)
        csvfile.write(',')
        csvfile.write(soiling + '\r\n')
except Exception as e:
    print(e)

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
with open(r'C:\DDS Data\modbusID.txt') as file:
    DeviceID = file.readline()
Readfunc = '03'
IDfunc = '06001faa'
year = int(time.strftime('%Y'))
year = hex(((year & 0xff) << 8) + (year >> 8))
year = year[2:]
year = year[2:4] + year[0:2]
year = year.zfill(4)
date = int(time.strftime('%m%d'))
date = hex(((date & 0xff) << 8) + (date >> 8))
date = date[2:]
date = date[2:4] + date[0:2]
date = date.zfill(4)

while True:
    try:
        inTi = time.time()
        Currentday = time.strftime('%y_%m_%d', time.localtime())
        if (today == Currentday):
            pass
        else:
            today = Currentday
            file = str(today + '_Soiling-data.txt')
            path = '%s\%s' % (r"C:\soft\soiling", file)
            year = int(time.strftime('%Y'))
            year = hex(((year & 0xff) << 8) + (year >> 8))
            year = year[2:]
            year = year[2:4] + year[0:2]
            year = year.zfill(4)
            date = int(time.strftime('%m%d'))
            date = hex(((date & 0xff) << 8) + (date >> 8))
            date = date[2:]
            date = date[2:4] + date[0:2]
            date = date.zfill(4)
            try:
                mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306,
                                               database="vena_dds_global")
                offsetini = open(r'C:\DDS Data\offset.ini', 'r')
                Line1 = offsetini.readlines()
                dasID = Line1[9].split(':')
                dasID = dasID[1].replace('\n', '')
                offsetini.close
                SQL = '%s%s%s' % ("SELECT date, soiling FROM ", dasID, ".Daily_soiling order by date desc limit 1")
                cursor = mydb.cursor()
                cursor.execute(SQL)
                data = cursor.fetchall()
                soiling = '%04d' % (math.floor(data[0][1] * 1000))
                with open(path, 'a+') as csvfile:
                    csvfile.write(today)
                    csvfile.write(',')
                    csvfile.write(soiling + '\r\n')
            except Exception as e:
                print(e)
        if serCOM2.inWaiting() > 0:
            command = serCOM2.read(10)
            commdata = command[0:6]
            inCrc = command[6:10]
            commandcrc = calc_crc(commdata.hex())
            if (command[0:1].hex() == DeviceID) & (command[1:5].hex() == IDfunc) & (commandcrc[0:4] == inCrc.hex()):
                print(time.strftime("%Y-%m-%d %H:%M:%S"), 'Data input: ', {command.hex()})
                DeviceID = command[5:6].hex()
                res = command[5:6].hex() + command[1:5].hex() + command[5:6].hex()
                rescrc = calc_crc(res)
                resData = bytes.fromhex(res + rescrc)
                serCOM2.write(resData)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), 'Data Output: ', {resData.hex()})
                with open(r'C:\DDS Data\modbusID.txt', 'w') as file:
                    file.write(DeviceID)
            if (command[0:1].hex() == DeviceID) & (command[1:2].hex() == Readfunc) & (commandcrc[0:4] == inCrc.hex()):
                print(time.strftime("%Y-%m-%d %H:%M:%S"), 'Data input: ', {command.hex()})
                rescrc = bytes.fromhex(DeviceID + Readfunc + year + date + soiling)
                rescrc = calc_crc(rescrc.hex())
                SendData = bytes.fromhex(DeviceID + Readfunc + '06' + year + date + soiling + rescrc)
                serCOM2.write(SendData)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), 'Data Output: ', {SendData.hex()})
        time.sleep(0.001)
    except Exception as e:
        print(e)


