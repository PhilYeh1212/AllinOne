import os
import csv
import math
import time
import serial
import mysql.connector

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
    return hex(((crc & 0xff) << 8) + (crc >> 8))

mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="vena_dds_global")
offsetini = open(r'C:\DDS Data\offset.ini', 'r')
Line1 = offsetini.readlines()
dasID = Line1[9].split(':')
dasID = dasID[1].replace('\n', '')
offsetini.close

SQL = '%s%s%s' % ("SELECT date, soiling FROM ", dasID, ".Daily_soiling order by date desc limit 1")
cursor = mydb.cursor()
cursor.execute(SQL)
data = cursor.fetchall()
soiling = '%02d' % (math.floor(data[0][1] * 100))
print(soiling)

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
DeviceID = '41'
fun = '03'

while True:
    Command = serCOM2.read(20)
    CommData = Command[0:6]
    inCrc = Command[6:10]
    crc = calc_crc(CommData.hex())
    print('CMD = ', Command)
    if Command[0:1].hex() == DeviceID:
        if Command[1:2].hex() == fun:
            if crc[2:6] == inCrc.hex():
                bufdata = '%s%s' % ('41030200', soiling)
                crcsend = calc_crc(bufdata)
                SendData = bytes.fromhex(bufdata + crcsend[2:6])
                serCOM2.write(SendData)
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), SendData)
