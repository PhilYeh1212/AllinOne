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
mydb = mysql.connector.connect(host="35.221.247.182", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
fivemin = 0
sitecode = []
Alarmall = ''
RAWline = ''
if not os.path.isdir('%s\%s' % (r'D:\FSLogger\temp', today)):
    os.mkdir('%s\%s' % (r'D:\FSLogger\temp', today))
with open(r'D:\FSLogger\FS102.csv', newline='') as csvfile:
#with open(r'C:\FS102.csv', newline='') as csvfile:
    row = csv.reader(csvfile, delimiter=',')
    inTI = time.time()
    if inTI - fivemin >= 300:
        for sitecode in row:
            try:
                if sitecode[0] == 'TW180928':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                                          ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX24, INVXX23, INVXX26, INVXX25, INVXX28, INVXX27, INVXX30, INVXX29, INVXX32, INVXX31, INVXX34, INVXX33'
                                          ',INVXX36, INVXX35, INVXX07 FROM FSLG_',sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ', str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    #print(irrins)
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000), INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], '#\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14], INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1])/1000)+'\n')
                            RAWline = RAWline + raw1
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15], INVdata[j][14], INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4])/1000)+'\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14], INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '4', INVdata[j][15], INVdata[j][14], INVdata[j][16], INVdata[j][17], '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17])/1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15], INVdata[j][14], INVdata[j][18], INVdata[j][19], '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '6', INVdata[j][15], INVdata[j][14], INVdata[j][20], INVdata[j][21], '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '7', INVdata[j][15], INVdata[j][14], INVdata[j][22], INVdata[j][23], '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '8', INVdata[j][15], INVdata[j][14], INVdata[j][24], INVdata[j][25], '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '9', INVdata[j][15], INVdata[j][14], INVdata[j][26], INVdata[j][27], '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27])/1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'A', INVdata[j][15], INVdata[j][14], INVdata[j][28], INVdata[j][29], '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29])/1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'B', INVdata[j][15], INVdata[j][14], INVdata[j][30], INVdata[j][31], '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31])/1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'C', INVdata[j][15], INVdata[j][14], INVdata[j][32], INVdata[j][33], '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33])/1000) + '\n')
                            RAWline = RAWline + raw12
                        else:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][0], INVdata[j][1],
                                    '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][3], INVdata[j][4],
                                    '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][9], INVdata[j][10],
                                    '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '4', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][16], INVdata[j][17],
                                    '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17]) / 1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                    '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19]) / 1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '6', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                    '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21]) / 1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '7', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                    '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23]) / 1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '8', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                    '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25]) / 1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '9', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][26], INVdata[j][27],
                                    '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27]) / 1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'A', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][28], INVdata[j][29],
                                     '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29]) / 1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'B', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][30], INVdata[j][31],
                                     '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31]) / 1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'C', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][32], INVdata[j][33],
                                     '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33]) / 1000) + '\n')
                            RAWline = RAWline + raw12
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw2 = ''
                    raw3 = ''
                    raw4 = ''
                    raw5 = ''
                    raw6 = ''
                    raw7 = ''
                    raw8 = ''
                    raw9 = ''
                    raw10 = ''
                    raw11 = ''
                    raw12 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'TW180929':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                                          ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX24, INVXX23, INVXX26, INVXX25, INVXX28, INVXX27, INVXX30, INVXX29, INVXX32, INVXX31, INVXX34, INVXX33'
                                          ',INVXX36, INVXX35, INVXX07 FROM FSLG_',sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ', str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    #print(irrins)
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], '#\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M2', inverternum, '1', INVdata[j][15], INVdata[j][14], INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1])/1000)+'\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M2', inverternum, '2', INVdata[j][15], INVdata[j][14], INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4])/1000)+'\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '3', INVdata[j][15], INVdata[j][14], INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '4', INVdata[j][15], INVdata[j][14], INVdata[j][16], INVdata[j][17], '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17])/1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '5', INVdata[j][15], INVdata[j][14], INVdata[j][18], INVdata[j][19], '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '6', INVdata[j][15], INVdata[j][14], INVdata[j][20], INVdata[j][21], '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '7', INVdata[j][15], INVdata[j][14], INVdata[j][22], INVdata[j][23], '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '8', INVdata[j][15], INVdata[j][14], INVdata[j][24], INVdata[j][25], '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '9', INVdata[j][15], INVdata[j][14], INVdata[j][26], INVdata[j][27], '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27])/1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, 'A', INVdata[j][15], INVdata[j][14], INVdata[j][28], INVdata[j][29], '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29])/1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, 'B', INVdata[j][15], INVdata[j][14], INVdata[j][30], INVdata[j][31], '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31])/1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, 'C', INVdata[j][15], INVdata[j][14], INVdata[j][32], INVdata[j][33], '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33])/1000) + '\n')
                            RAWline = RAWline + raw12
                        else:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '1', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][0], INVdata[j][1],
                                    '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '2', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][3], INVdata[j][4],
                                    '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '3', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][9], INVdata[j][10],
                                    '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '4', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][16], INVdata[j][17],
                                    '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17]) / 1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '5', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                    '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19]) / 1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '6', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                    '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21]) / 1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '7', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                    '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23]) / 1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '8', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                    '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25]) / 1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, '9', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][26], INVdata[j][27],
                                    '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27]) / 1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, 'A', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][28], INVdata[j][29],
                                     '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29]) / 1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, 'B', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][30], INVdata[j][31],
                                     '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31]) / 1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M2', inverternum, 'C', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][32], INVdata[j][33],
                                     '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33]) / 1000) + '\n')
                            RAWline = RAWline + raw12
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw2 = ''
                    raw3 = ''
                    raw4 = ''
                    raw5 = ''
                    raw6 = ''
                    raw7 = ''
                    raw8 = ''
                    raw9 = ''
                    raw10 = ''
                    raw11 = ''
                    raw12 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'TW180931':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                                          ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX24, INVXX23, INVXX26, INVXX25, INVXX28, INVXX27, INVXX30, INVXX29, INVXX32, INVXX31, INVXX34, INVXX33'
                                          ',INVXX36, INVXX35, INVXX07 FROM FSLG_',sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ', str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    #print(irrins)
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][16], '#\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M4', inverternum, '1', INVdata[j][15], INVdata[j][14], INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1])/1000)+'\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M4', inverternum, '2', INVdata[j][15], INVdata[j][14], INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4])/1000)+'\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '3', INVdata[j][15], INVdata[j][14], INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '4', INVdata[j][15], INVdata[j][14], INVdata[j][16], INVdata[j][17], '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17])/1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '5', INVdata[j][15], INVdata[j][14], INVdata[j][18], INVdata[j][19], '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '6', INVdata[j][15], INVdata[j][14], INVdata[j][20], INVdata[j][21], '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '7', INVdata[j][15], INVdata[j][14], INVdata[j][22], INVdata[j][23], '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '8', INVdata[j][15], INVdata[j][14], INVdata[j][24], INVdata[j][25], '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '9', INVdata[j][15], INVdata[j][14], INVdata[j][26], INVdata[j][27], '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27])/1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, 'A', INVdata[j][15], INVdata[j][14], INVdata[j][28], INVdata[j][29], '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29])/1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, 'B', INVdata[j][15], INVdata[j][14], INVdata[j][30], INVdata[j][31], '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31])/1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, 'C', INVdata[j][15], INVdata[j][14], INVdata[j][32], INVdata[j][33], '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33])/1000) + '\n')
                            RAWline = RAWline + raw12
                        else:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '1', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][0], INVdata[j][1],
                                    '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '2', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][3], INVdata[j][4],
                                    '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '3', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][9], INVdata[j][10],
                                    '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '4', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][16], INVdata[j][17],
                                    '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17]) / 1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '5', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                    '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19]) / 1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '6', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                    '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21]) / 1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '7', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                    '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23]) / 1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '8', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                    '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25]) / 1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, '9', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][26], INVdata[j][27],
                                    '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27]) / 1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, 'A', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][28], INVdata[j][29],
                                     '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29]) / 1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, 'B', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][30], INVdata[j][31],
                                     '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31]) / 1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M4', inverternum, 'C', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][32], INVdata[j][33],
                                     '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33]) / 1000) + '\n')
                            RAWline = RAWline + raw12
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw2 = ''
                    raw3 = ''
                    raw4 = ''
                    raw5 = ''
                    raw6 = ''
                    raw7 = ''
                    raw8 = ''
                    raw9 = ''
                    raw10 = ''
                    raw11 = ''
                    raw12 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'TW180930':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                                          ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX24, INVXX23, INVXX26, INVXX25, INVXX28, INVXX27, INVXX30, INVXX29, INVXX32, INVXX31, INVXX34, INVXX33'
                                          ',INVXX36, INVXX35, INVXX07 FROM FSLG_',sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ', str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    #print(irrins)
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], '#\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M3', inverternum, '1', INVdata[j][15], INVdata[j][14], INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1])/1000)+'\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0]+'01', sitecode[0] + 'M3', inverternum, '2', INVdata[j][15], INVdata[j][14], INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4])/1000)+'\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '3', INVdata[j][15], INVdata[j][14], INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '4', INVdata[j][15], INVdata[j][14], INVdata[j][16], INVdata[j][17], '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17])/1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '5', INVdata[j][15], INVdata[j][14], INVdata[j][18], INVdata[j][19], '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '6', INVdata[j][15], INVdata[j][14], INVdata[j][20], INVdata[j][21], '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '7', INVdata[j][15], INVdata[j][14], INVdata[j][22], INVdata[j][23], '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '8', INVdata[j][15], INVdata[j][14], INVdata[j][24], INVdata[j][25], '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '9', INVdata[j][15], INVdata[j][14], INVdata[j][26], INVdata[j][27], '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27])/1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, 'A', INVdata[j][15], INVdata[j][14], INVdata[j][28], INVdata[j][29], '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29])/1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, 'B', INVdata[j][15], INVdata[j][14], INVdata[j][30], INVdata[j][31], '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31])/1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, 'C', INVdata[j][15], INVdata[j][14], INVdata[j][32], INVdata[j][33], '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33])/1000) + '\n')
                            RAWline = RAWline + raw12
                        else:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][34], INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '1', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][0], INVdata[j][1],
                                    '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '2', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][3], INVdata[j][4],
                                    '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '3', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][9], INVdata[j][10],
                                    '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '4', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][16], INVdata[j][17],
                                    '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17]) / 1000) + '\n')
                            RAWline = RAWline + raw4
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '5', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                    '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19]) / 1000) + '\n')
                            RAWline = RAWline + raw5
                            raw6 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '6', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                    '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21]) / 1000) + '\n')
                            RAWline = RAWline + raw6
                            raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '7', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                    '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23]) / 1000) + '\n')
                            RAWline = RAWline + raw7
                            raw8 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '8', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                    '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25]) / 1000) + '\n')
                            RAWline = RAWline + raw8
                            raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, '9', INVdata[j][15],
                                    INVdata[j][14], INVdata[j][26], INVdata[j][27],
                                    '%.2f' % (float(INVdata[j][26]) * float(INVdata[j][27]) / 1000) + '\n')
                            RAWline = RAWline + raw9
                            raw10 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, 'A', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][28], INVdata[j][29],
                                     '%.2f' % (float(INVdata[j][28]) * float(INVdata[j][29]) / 1000) + '\n')
                            RAWline = RAWline + raw10
                            raw11 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, 'B', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][30], INVdata[j][31],
                                     '%.2f' % (float(INVdata[j][30]) * float(INVdata[j][31]) / 1000) + '\n')
                            RAWline = RAWline + raw11
                            raw12 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                    (sitecode[0] + '01', sitecode[0] + 'M3', inverternum, 'C', INVdata[j][15],
                                     INVdata[j][14], INVdata[j][32], INVdata[j][33],
                                     '%.2f' % (float(INVdata[j][32]) * float(INVdata[j][33]) / 1000) + '\n')
                            RAWline = RAWline + raw12
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw2 = ''
                    raw3 = ''
                    raw4 = ''
                    raw5 = ''
                    raw6 = ''
                    raw7 = ''
                    raw8 = ''
                    raw9 = ''
                    raw10 = ''
                    raw11 = ''
                    raw12 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'TW180807' or sitecode[0] == 'TW180932':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % (
                    'SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                    ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX07 FROM FSLG_', sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ',
                    str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    # print(irrins)
                    S001 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0] + '01', sitecode[0] + 'S001', irrins[0][3], irrins[0][2], irrins[0][1], '\n')
                    S002 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0] + '01', sitecode[0] + 'S002', irrins[0][3], irrins[0][2], irrins[0][0], '\n')
                    RAWline = S001 + S002
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            if inverternum <= 9:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][20], '#\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14],INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                            else:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][20], '#\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '1', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][0], INVdata[j][1],
                                           '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '3', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][9], INVdata[j][10],
                                           '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                        else:
                            if inverternum <= 9:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][20], INVdata[j][12] + '\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14],INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                            else:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][20], INVdata[j][12] + '\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '1', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][0], INVdata[j][1],
                                           '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '3', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][9], INVdata[j][10],
                                           '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw3 = ''
                    raw5 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'TW180933' or sitecode[0] == 'TW180792' or sitecode[0] == 'TW180796':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % (
                    'SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                    ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX26, INVXX25, INVXX30, INVXX29, INVXX34, INVXX33, INVXX07 FROM FSLG_', sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ', str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    # print(irrins)
                    S001 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0] + '01', sitecode[0] + 'S001', irrins[0][3], irrins[0][2], irrins[0][1], '\n')
                    S002 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0] + '01', sitecode[0] + 'S002', irrins[0][3], irrins[0][2], irrins[0][0], '\n')
                    RAWline = S001 + S002
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            if inverternum <= 9:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][26], '#\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14],INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                                raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '7', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                           '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                                RAWline = RAWline + raw7
                                raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '9', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                           '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                                RAWline = RAWline + raw9
                                rawB = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'B', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                           '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                                RAWline = RAWline + rawB
                            else:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][26], '#\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '1', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][0], INVdata[j][1],
                                           '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '3', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][9], INVdata[j][10],
                                           '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                                raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '7', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                           '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                                RAWline = RAWline + raw7
                                raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '9', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                           '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                                RAWline = RAWline + raw9
                                rawB = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, 'B', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                           '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                                RAWline = RAWline + rawB
                        else:
                            if inverternum <= 9:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][26], INVdata[j][12] + '\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14],
                                       INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14],INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                                raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '7', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                           '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                                RAWline = RAWline + raw7
                                raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '9', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                           '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                                RAWline = RAWline + raw9
                                rawB = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M0', inverternum, 'B', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                           '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                                RAWline = RAWline + rawB
                            else:
                                raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '0', INVdata[j][15],
                                           INVdata[j][14],
                                           '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                           INVdata[j][7],
                                           (INVdata[j][8] + '###'), INVdata[j][26], INVdata[j][12] + '\n')
                                RAWline = RAWline + raw0
                                raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '1', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][0], INVdata[j][1],
                                           '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                                RAWline = RAWline + raw1
                                raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '3', INVdata[j][15],
                                           INVdata[j][14],
                                           INVdata[j][9], INVdata[j][10],
                                           '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                                RAWline = RAWline + raw3
                                raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '5', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                           '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                                RAWline = RAWline + raw5
                                raw7 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '7', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][20], INVdata[j][21],
                                           '%.2f' % (float(INVdata[j][20]) * float(INVdata[j][21])/1000) + '\n')
                                RAWline = RAWline + raw7
                                raw9 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, '9', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][22], INVdata[j][23],
                                           '%.2f' % (float(INVdata[j][22]) * float(INVdata[j][23])/1000) + '\n')
                                RAWline = RAWline + raw9
                                rawB = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                       (
                                           sitecode[0] + '01', sitecode[0] + 'M', inverternum, 'B', INVdata[j][15],
                                           INVdata[j][14], INVdata[j][24], INVdata[j][25],
                                           '%.2f' % (float(INVdata[j][24]) * float(INVdata[j][25])/1000) + '\n')
                                RAWline = RAWline + rawB
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw3 = ''
                    raw5 = ''
                    raw7 = ''
                    raw9 = ''
                    rawB = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'TW180805':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % (
                    'SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                    ',INVXX17, INVXX16, INVXX22, INVXX21, INVXX07 FROM FSLG_', sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ',
                    str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    # print(irrins)
                    S001 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0] + '01', sitecode[0] + 'S001', irrins[0][3], irrins[0][2], irrins[0][1], '\n')
                    S002 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0] + '01', sitecode[0] + 'S002', irrins[0][3], irrins[0][2], irrins[0][0], '\n')
                    RAWline = S001 + S002
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][20], '#\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                   sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],
                                   INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][3], INVdata[j][4],
                                       '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                   sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14],
                                   INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                       INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                       '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19])/1000) + '\n')
                            RAWline = RAWline + raw5
                        else:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),
                                       INVdata[j][7],
                                       (INVdata[j][8] + '###'), INVdata[j][20], INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '1', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1],
                                       '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '2', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][3], INVdata[j][4],
                                       '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '3', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][9], INVdata[j][10],
                                       '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw5 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0] + '01', sitecode[0] + 'M0', inverternum, '5', INVdata[j][15],
                                       INVdata[j][14], INVdata[j][18], INVdata[j][19],
                                       '%.2f' % (float(INVdata[j][18]) * float(INVdata[j][19]) / 1000) + '\n')
                            RAWline = RAWline + raw5
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw2 = ''
                    raw3 = ''
                    raw5 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'FS200700402':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % (
                    'SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                    ',INVXX17, INVXX16, INVXX19, INVXX20, INVXX07 FROM FSLG_', sitecode[0], 'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ',
                    str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    #print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    # print(irrins)
                    S001 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0], sitecode[0][0:9] + 'S001', irrins[0][3], irrins[0][2], irrins[0][1], '\n')
                    S002 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0], sitecode[0][0:9] + 'S002', irrins[0][3], irrins[0][2], irrins[0][0], '\n')
                    RAWline = S001 + S002
                    for j in range(num):
                        inverternum = j + 1
                        if float(INVdata[j][12]) <= 0:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '0', INVdata[j][15],INVdata[j][14],'####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),INVdata[j][7],(INVdata[j][8] + '###'), INVdata[j][20], '#\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '2', INVdata[j][15], INVdata[j][14],INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14], INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '5', INVdata[j][15], INVdata[j][14], INVdata[j][16], INVdata[j][17], '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17]) / 1000) + '\n')
                        else:
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '0', INVdata[j][15],INVdata[j][14],'####' + INVdata[j][5], INVdata[j][6], str(float(INVdata[j][2]) / 1000),INVdata[j][7],(INVdata[j][8] + '###'), INVdata[j][20], INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '1', INVdata[j][15], INVdata[j][14],INVdata[j][0], INVdata[j][1], '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '2', INVdata[j][15],INVdata[j][14],INVdata[j][3], INVdata[j][4], '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '3', INVdata[j][15], INVdata[j][14],INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                            raw4 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '5', INVdata[j][15],INVdata[j][14], INVdata[j][16], INVdata[j][17], '%.2f' % (float(INVdata[j][16]) * float(INVdata[j][17]) / 1000) + '\n')
                            RAWline = RAWline + raw4
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                    raw0 = ''
                    raw1 = ''
                    raw2 = ''
                    raw3 = ''
                    raw5 = ''
                    S001 = ''
                    S002 = ''
                    RAWline = ''
                    Alarmall = ''
                if sitecode[0] == 'FS200700401':
                    sql1 = "%s%s.%s" % ('SELECT Irr, T_PV, daq_time, daq_date FROM FSLG_', sitecode[0],
                                        'T1_head Order by daq_date desc, daq_time desc Limit 1')
                    num = int(sitecode[1])
                    # print(num)
                    sql2 = "%s%s.%s%s" % (
                        'SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03, daq_time, daq_date'
                        ',INVXX17, INVXX16, INVXX20, INVXX19, INVXX07 FROM FSLG_', sitecode[0],
                        'T2_inv Order by daq_date desc, daq_time desc, INVID asc Limit ',
                        str(sitecode[1]))
                    cursor1 = mydb.cursor()
                    cursor1.execute(sql1)
                    irrins = cursor1.fetchall()
                    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    # print(timenow, sql2)
                    cursor2 = mydb.cursor()
                    cursor2.execute(sql2)
                    INVdata = cursor2.fetchall()
                    # print(irrins)
                    S001 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0], sitecode[0][0:9] + 'S001', irrins[0][3], irrins[0][2], irrins[0][1], '\n')
                    S002 = '%s#%s#%s %s#%s%s' % (
                        sitecode[0], sitecode[0][0:9] + 'S002', irrins[0][3], irrins[0][2], irrins[0][0], '\n')
                    RAWline = S001 + S002
                    for j in range(num):
                        if float(INVdata[j][12]) <= 0:
                            inverternum = j + 1
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', '4', '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + str(INVdata[j][5]), str(INVdata[j][6]),
                                       str(float(INVdata[j][2]) / 1000),
                                       str(INVdata[j][7]), (str(INVdata[j][8]) + '###'), INVdata[j][20], '#' + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', '4', '1', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1],
                                       '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', '4', '2', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][3], INVdata[j][4],
                                       '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', '4', '3', INVdata[j][15], INVdata[j][14], INVdata[j][9], INVdata[j][10], '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                        else:
                            inverternum = j + 1
                            raw0 = '%s#%s%s%s#%s %s#%s#%s#%s#%s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '0', INVdata[j][15],
                                       INVdata[j][14],
                                       '####' + str(INVdata[j][5]), str(INVdata[j][6]),
                                       str(float(INVdata[j][2]) / 1000),
                                       str(INVdata[j][7]), (str(INVdata[j][8]) + '###'), INVdata[j][20],
                                       INVdata[j][12] + '\n')
                            RAWline = RAWline + raw0
                            raw1 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '1', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][0], INVdata[j][1],
                                       '%.2f' % (float(INVdata[j][0]) * float(INVdata[j][1]) / 1000) + '\n')
                            RAWline = RAWline + raw1
                            raw2 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '2', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][3], INVdata[j][4],
                                       '%.2f' % (float(INVdata[j][3]) * float(INVdata[j][4]) / 1000) + '\n')
                            RAWline = RAWline + raw2
                            raw3 = '%s#%s%s%s#%s %s#%s#%s#%s' % \
                                   (
                                       sitecode[0], sitecode[0][0:9] + 'M0', inverternum, '2', INVdata[j][15],
                                       INVdata[j][14],
                                       INVdata[j][9], INVdata[j][10],
                                       '%.2f' % (float(INVdata[j][9]) * float(INVdata[j][10]) / 1000) + '\n')
                            RAWline = RAWline + raw3
                    with open('%s\%s\%s_%s_%s.%s' % (r'D:\FSLogger\temp', today, 'API_Log', today, sitecode[0], 'txt'),
                              'a+') as RAWtxt:
                        RAWtxt.write(RAWline)
                    uploadlist1 = session.post(URL1, RAWline)
                    print(timenow, sitecode[0], uploadlist1)
                raw0 = ''
                raw1 = ''
                raw2 = ''
                raw3 = ''
                raw5 = ''
                S001 = ''
                S002 = ''
                RAWline = ''
                Alarmall = ''
            except Exception as e:
                print(e)
