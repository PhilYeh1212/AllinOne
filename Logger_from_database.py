import os
import csv
import time
import requests
import mysql.connector

print('Version-1.2')
session = requests.session()
today = time.strftime('%y%m%d', time.localtime())
URL1 = 'https://pmsdata.formosasolar.com.tw/realtime/extel'
URL2 = 'https://pmsdata.formosasolar.com.tw/realtime/extel/alarm'
mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
fivemin = 0
sitecode = []
raw00 = ''
raw11 = ''
raw22 = ''
Alarmall = ''
if not os.path.isdir('%s\%s' % (r'C:\_Phil\temp', today)):
    os.mkdir('%s\%s' % (r'C:\_Phil\temp', today))
with open(r'C:\FS100.csv', newline='') as csvfile:
    row = csv.reader(csvfile, delimiter=',')

    inTI = time.time()
    if inTI - fivemin >= 300:
        for sitecode in row:
            #print(sitecode[0])
            try:
                #print(sitecode[i])
                #print(sitecode[i+1)
                sql1 = "%s%s.%s" % ('SELECT Irr, T_PV FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                num = int(sitecode[1])
                # print(num)
                sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date FROM FSLG_',sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc Limit ', str(sitecode[1]))
                cursor1 = mydb.cursor()
                cursor1.execute(sql1)
                irrins = cursor1.fetchall()
                timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(timenow, sql2)
                cursor2 = mydb.cursor()
                cursor2.execute(sql2)
                INVdata = cursor2.fetchall()
                #print(irrins)
                S001 = '%s#%s#%s#%s%s' % (sitecode[0]+'01', sitecode[0] + 'S001', Today, irrins[0][1], '\n')
                S002 = '%s#%s#%s#%s%s' % (sitecode[0]+'01', sitecode[0] + 'S002', Today, irrins[0][0], '\n')
                RAWline = S001 + S002
                for j in range(num):
                    inverternum = j + 1
                    raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s' % \
                           (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15], INVdata[j][14], '####' + str(INVdata[j][5]), str(INVdata[j][6]), str((INVdata[j][2]/1000)), str(INVdata[j][7]), (str(INVdata[j][8])+'###\n'))
                    RAWline = RAWline + raw0
                    raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                           (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14], INVdata[j][0], INVdata[j][1], '%.2f' % ((INVdata[j][0] * INVdata[j][1])/1000)+'\n')
                    RAWline = RAWline + raw1
                    raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                           (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15], INVdata[j][14], INVdata[j][3], INVdata[j][4], '%.2f' % ((INVdata[j][3] * INVdata[j][4])/1000)+'\n')
                    RAWline = RAWline + raw2
                    if INVdata[j][12] <= 0:
                        Alarmcode = INVdata[j][12]
                        if Alarmcode <= 0:
                            Alarmcode = 0
                        else:
                            pass
                        Alarm = '%s#%s#%s %s#%s#%s%s' % \
                                (sitecode[0] + '01', sitecode[0] + 'M010', INVdata[j][15], INVdata[j][14], 'CLEAR', Alarmcode, '\n')
                        Alarmall = Alarmall + Alarm
                    else:
                        Alarm = '%s#%s#%s %s#%s#%s%s' % \
                                (sitecode[0] + '01', sitecode[0] + 'M010', INVdata[j][15], INVdata[j][14], 'START', Alarmcode, '\n')
                        Alarmall = Alarmall + Alarm

                    #print(RAWline)
                with open('%s\%s\%s_%s_%s.%s' % (r'C:\_Phil\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                          'a+') as RAWtxt:
                    RAWtxt.write(RAWline)
                with open('%s\%s\%s_%s_%s.%s' % (r'C:\_Phil\temp', today, 'API_Log_Alarm', today, sitecode[0],  'txt'),
                          'a+') as ALMtxt:
                    ALMtxt.write(Alarmall)
                    #uploadlist1 = session.post(URL1, RAWline)
                    #uploadlist2 = session.post(URL2, Alarmall)
                    #print(timenow, sitecode[i], uploadlist1)
                    #print(timenow, sitecode[i], uploadlist2)
                raw0 = ''
                raw1 = ''
                raw2 = ''
                S001 = ''
                S002 = ''
                RAWline = ''
                Alarmall = ''
            except Exception as e:
                print(e)
        fivemin = time.time()
        LastTi = time.time()
        timeall = inTI - LastTi
        print(timeall)