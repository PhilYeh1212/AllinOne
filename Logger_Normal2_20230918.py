import os
import csv
import time
import requests
from datetime import datetime, timedelta
import mysql.connector

print('Version-1.2')
session = requests.session()
today = time.strftime('%y%m%d', time.localtime())
URL1 = 'https://pmsdata.formosasolar.com.tw/realtime/extel'
URL2 = 'https://pmsdata.formosasolar.com.tw/realtime/extel/alarm'
#mydb = mysql.connector.connect(host="35.221.247.182", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
fivemin = 0
sitecode = []
raw00 = ''
raw11 = ''
raw22 = ''
Alarmall = ''
if not os.path.isdir('%s\%s' % (r'D:\FSLogger\temp', today)):
    os.mkdir('%s\%s' % (r'D:\FSLogger\temp', today))
with open(r'D:\FSLogger\FS104.csv', newline='') as csvfile:
# with open(r'C:\\FS100.csv', newline='') as csvfile:
    row = csv.reader(csvfile, delimiter=',')
    for sitecode in row:
        try:
            DB = '%s%s' %('FSLG_', sitecode[0])
            mydb = mysql.connector.connect(host="35.221.247.182", user="root", password="Oerlikon;1234", port=3306,
                                       database=DB)
            sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
            num = int(sitecode[1])
            #sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date FROM FSLG_',sitecode[0], 'T2_inv Order by daq_date desc, daq_time >= %s, INVID asc Limit ', str(sitecode[1]))
            sql2 = """
            SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, 
            INVXX01, INVXX02, INVXX03, daq_time, daq_date, INVXX07
             FROM T2_inv
            WHERE
                daq_date = DATE_FORMAT(NOW(), '%Y/%m/%d')
                AND daq_time < DATE_FORMAT(NOW(), '%H:%i:00')
                AND daq_time > DATE_FORMAT(NOW() - INTERVAL 10 MINUTE, '%h:%i:%s')
            ORDER BY keyID desc, invid desc
        """
            cursor1 = mydb.cursor()
            cursor1.execute(sql1)
            irrins = cursor1.fetchall()
            timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #print(timenow, sql2)
            cursor2 = mydb.cursor()
            cursor2.execute(sql2)
            INVdata = cursor2.fetchall()
            INVdata.reverse()
            #print(INVdata)
            S001 = '%s#%s#%s %s#%s%s' % (
                sitecode[0] + '01', sitecode[0] + 'S001', irrins[0][3], irrins[0][2], irrins[0][1], '\n')
            S002 = '%s#%s#%s %s#%s%s' % (
                sitecode[0] + '01', sitecode[0] + 'S002', irrins[0][3], irrins[0][2], irrins[0][0], '\n')
            RAWline = S001 + S002
            for j in range(num):
                inverternum = j + 1
                kWh = str(float(INVdata[j][2]) / 1000)
                if float(INVdata[j][12]) <= 0:
                    if inverternum <= 9:
                        raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                               (
                               sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15], INVdata[j][14],
                               '####' + INVdata[j][5], INVdata[j][6], str(kWh), INVdata[j][7],
                               (INVdata[j][8] + '###'), INVdata[j][16], '#\n')
                        RAWline = RAWline + raw0
                        raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1])/1000)+'\n')
                        RAWline = RAWline + raw1
                        raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15], INVdata[j][14],
                                INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4])/1000)+'\n')
                        RAWline = RAWline + raw2
                    else:
                        raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                               (sitecode[0] + '01', sitecode[0] + 'M', inverternum, '0', INVdata[j][15], INVdata[j][14],
                               '####' + INVdata[j][5], INVdata[j][6], str(kWh), INVdata[j][7],
                                (INVdata[j][8] + '###'), INVdata[j][16], '#\n')
                        RAWline = RAWline + raw0
                        raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (
                               sitecode[0] + '01', sitecode[0] + 'M', inverternum, '1', INVdata[j][15], INVdata[j][14],
                               INVdata[j][0], INVdata[j][1], '%.2f' % ((float(INVdata[j][0]) * float(INVdata[j][1])) / 1000) + '\n')
                        RAWline = RAWline + raw1
                        raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (
                               sitecode[0] + '01', sitecode[0] + 'M', inverternum, '2', INVdata[j][15], INVdata[j][14],
                               INVdata[j][3], INVdata[j][4], '%.2f' % ((float(INVdata[j][3]) * float(INVdata[j][4])) / 1000) + '\n')
                        RAWline = RAWline + raw2
                else:
                    if inverternum <= 9:
                        raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                               (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15], INVdata[j][14],
                                '####' + INVdata[j][5], INVdata[j][6], str(kWh), INVdata[j][7],
                                (INVdata[j][8]+'###'), INVdata[j][16], INVdata[j][12]+'\n')
                        RAWline = RAWline + raw0
                        raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1])/1000)+'\n')
                        RAWline = RAWline + raw1
                        raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15], INVdata[j][14],
                                INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4])/1000)+'\n')
                        RAWline = RAWline + raw2
                    else:
                        raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                               (sitecode[0] + '01', sitecode[0] + 'M', inverternum, '0', INVdata[j][15], INVdata[j][14],
                               '####' + INVdata[j][5], INVdata[j][6], str(kWh), INVdata[j][7],
                                (INVdata[j][8] + '###'), INVdata[j][16], INVdata[j][12]+'\n')
                        RAWline = RAWline + raw0
                        raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (
                               sitecode[0] + '01', sitecode[0] + 'M', inverternum, '1', INVdata[j][15], INVdata[j][14],
                               INVdata[j][0], INVdata[j][1], '%.2f' % ((float(INVdata[j][0]) * float(INVdata[j][1])) / 1000) + '\n')
                        RAWline = RAWline + raw1
                        raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                               (
                               sitecode[0] + '01', sitecode[0] + 'M', inverternum, '2', INVdata[j][15], INVdata[j][14],
                               INVdata[j][3], INVdata[j][4], '%.2f' % ((float(INVdata[j][3]) * float(INVdata[j][4])) / 1000) + '\n')
                        RAWline = RAWline + raw2
            with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                      'a+') as RAWtxt:
                RAWtxt.write(RAWline)
            uploadlist1 = session.post(URL1, RAWline)
            print(timenow, sitecode[0], uploadlist1)
            raw0 = ''
            raw1 = ''
            raw2 = ''
            S001 = ''
            S002 = ''
            RAWline = ''
        except Exception as e:
            print(e)