import time
import requests
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
sitecode = []
with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        #try:
        sitecode.append(f.readline().replace('\n', ''))
        sql1 = "%s%s.%s" % ('SELECT Irr, T_PV FROM FSLG_', sitecode[i], 'T1_head Order by daq_date desc, daq_time desc Limit 1')
        sql3 = "%s%s.%s" % ('SELECT max(INVID) FROM FSLG_', sitecode[i], 'T2_inv')
        #print(sql2)
        cursor3 = mydb.cursor()
        cursor3.execute(sql3)
        INVnum = cursor3.fetchall()
        print(INVnum[0][0])
        cursor1 = mydb.cursor()
        cursor1.execute(sql1)
        irrins = cursor1.fetchall()
        #print(irrins)
        S001 = '%s#%s#%s#%s' % (sitecode[i]+'01', sitecode[i] + '01S001', Today, irrins[0][1])
        S002 = '%s#%s#%s#%s' % (sitecode[i]+'01', sitecode[i] + '01S002', Today, irrins[0][0])
        if INVnum[0][0] == 3:
            sql2 = "%s%s.%s%s" % ('SELECT INVXX11, INVXX10, INVXX08, INVXX13, INVXX12, INVXX20, INVXX19, INVXX18, INVXX05, INVXX15, INVXX14, INVXX01, INVXX02, INVXX03 FROM FSLG_', sitecode[i], 'T2_inv Order by daq_date desc, daq_time desc Limit ', str(INVnum[0][0]))
            print(sql2)
            cursor2 = mydb.cursor()
            cursor2.execute(sql2)
            INVdata = cursor2.fetchall()
            M010 = '%s#%s#%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i]+'01', sitecode[i] + '01M010', Today, '####' + str(INVdata[0][5]), str(INVdata[0][6]), str(INVdata[0][2]), str(INVdata[0][7]), (str(INVdata[0][8])+'###'))
            M011 = '%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i]+'01', sitecode[i] + '01M011', Today, INVdata[0][0], INVdata[0][1], '%.2f' % ((INVdata[0][0] * INVdata[0][1])/1000))
            M012 = '%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i]+'01', sitecode[i] + '01M012', Today, INVdata[0][3], INVdata[0][4], '%.2f' % ((INVdata[0][0] * INVdata[0][1])/1000))

            M020 = '%s#%s#%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i]+'01', sitecode[i] + '01M020', Today, '####' + str(INVdata[1][5]), str(INVdata[1][6]), str(INVdata[1][2]), str(INVdata[1][7]), (str(INVdata[1][8])+'###'))
            M021 = '%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i]+'01', sitecode[i] + '01M021', Today, INVdata[1][0], INVdata[1][1], '%.2f' % ((INVdata[1][0] * INVdata[1][1])/1000))
            M022 = '%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i]+'01', sitecode[i] + '01M022', Today, INVdata[1][3], INVdata[1][4], '%.2f' % ((INVdata[1][0] * INVdata[1][1])/1000))

            M030 = '%s#%s#%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i] + '01', sitecode[i] + '01M020', Today, '####' + str(INVdata[2][5]),str(INVdata[2][6]), str(INVdata[2][2]), str(INVdata[2][7]), (str(INVdata[2][8]) + '###'))
            M031 = '%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i] + '01', sitecode[i] + '01M021', Today, INVdata[2][0], INVdata[2][1],'%.2f' % ((INVdata[2][0] * INVdata[2][1]) / 1000))
            M032 = '%s#%s#%s#%s#%s#%s' % \
                   (sitecode[i] + '01', sitecode[i] + '01M022', Today, INVdata[2][3], INVdata[2][4],'%.2f' % ((INVdata[2][0] * INVdata[2][1]) / 1000))
            print(int(INVdata[0][12]))
            if INVdata[0][12] != 0 or INVdata[1][12] != 0 or INVdata[2][12] != 0:
                Alarm01 = '%s#%s#%s#%s#%s' % \
                          (sitecode[i] + '01', sitecode[i] + '01M010', Today, 'START', str(INVdata[0][12]))
                Alarm02 = '%s#%s#%s#%s#%s' % \
                          (sitecode[i] + '01', sitecode[i] + '01M010', Today, 'START', str(INVdata[1][12]))
                Alarm03 = '%s#%s#%s#%s#%s' % \
                          (sitecode[i] + '01', sitecode[i] + '01M010', Today, 'START', str(INVdata[2][12]))
            else:
                Alarm01 = '%s#%s#%s#%s#%s' % \
                       (sitecode[i]+'01', sitecode[i] + '01M010', Today, 'CLEAR', int(INVdata[0][12]))
                Alarm02 = '%s#%s#%s#%s#%s' % \
                          (sitecode[i] + '01', sitecode[i] + '01M010', Today, 'CLEAR', str(INVdata[1][12]))
                Alarm03 = '%s#%s#%s#%s#%s' % \
                          (sitecode[i] + '01', sitecode[i] + '01M010', Today, 'CLEAR', str(INVdata[2][12]))
        # except Exception as e:
        #     print(e)