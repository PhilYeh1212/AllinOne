import time
import requests
import mysql.connector
#aUGMBQKt3BvG82Ymd0jcrnI6Ec9HxRZ6UxGCsglndeB
token = '4cwTgoUM0Npnnob1D0aUHCYWxN6huiqVF9poI0G1Efe'

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

data = []
Notupload = []
mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d', time.localtime())
sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
cursor1 = mydb.cursor()
cursor1.execute(sql1)
Online = cursor1.fetchall()

for k in Online:
    Extel_code = k
    Notupload.append(Extel_code[0])

num = len(Notupload)

if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if num > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = ((('未正常上傳案場共'+str(num)+'場'), sorted(Notupload)))
    lineNotifyMessage(token, message)


StartTime = '00:00:00'
EndTime = '05:00:00'
NightPower = []
NightPower1 = []
NightPowerError =[]
k = 0
#print(Today)

sitecode = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode.append(f.readline().replace('\n', ''))
        #sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
        sql2 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode[i], 'T2_inv where INVXX08 > 100', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        sql3 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        #sql1 = "SELECT Extel_code FROM FS_Logger_Global.Site_list where Instant_Power = 0"

        cursor1 = mydb.cursor()
        cursor1.execute(sql2)
        Online = cursor1.fetchall()
        if not Online:
            pass
        else:
            data = sitecode[i]
            NightPower.append(data)
    cursor2 = mydb.cursor()
    cursor2.execute(sql3)
    FS100 = cursor2.fetchall()
    for q in range(len(FS100)):
        for w in range(len(NightPower)):
            if (FS100[q][0] == NightPower[w]):
                NightPower1.append(FS100[q])
    while k < len(NightPower1):
        NightPowerError.append(NightPower1[k][1])
        k = k + 1

    num = len(NightPowerError)

    if num <= 0:
        message = "OK"
        lineNotifyMessage(token, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('夜間Inverter有讀值案場'+str(num)+'場'), sorted(NightPowerError)))
        lineNotifyMessage(token, message)


Zero = []
#sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
sql4 = "SELECT Extel_code FROM FS_Logger_Global.Site_list where Instant_Power = 0"

cursor1 = mydb.cursor()
cursor1.execute(sql4)
Online = cursor1.fetchall()
print(Online)

for k in Online:
    Extel_code = k
    Zero.append(Extel_code[0])

num = len(Zero)

if num <= 0:
    message = "OK"
    lineNotifyMessage(token, message)
if num > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = ((('Inverter功率讀值為零的案場共'+str(num)+'台'), sorted(Notupload)))
    lineNotifyMessage(token, message)

StartTime = '15:00:00'
EndTime = '15:00:00'
NightPower = []
sitenum = []
NightPowerError =[]
k = 0
#print(Today)
data = []
sitecode = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0, 100):
        sitecode.append(f.readline().replace('\n', ''))
        sql5 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID, INVXX02, INVXX03 FROM FSLG_', sitecode[i], 'T2_inv where (INVXX02 > 0 or INVXX03 > 0 and INVXX03 < 100) ' , 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        sql6 = "SELECT Site_code, Extel_code, inverter FROM FS_Logger_Global.Site_list"
        #sql1 = "SELECT Extel_code FROM FS_Logger_Global.Site_list where Instant_Power = 0"
        print(sql1)
        cursor1 = mydb.cursor()
        cursor1.execute(sql5)
        Online = cursor1.fetchall()
        cursor2 = mydb.cursor()
        cursor2.execute(sql6)
        FS100 = cursor2.fetchall()
        if not Online:
            pass
        else:
            data, Invcode = sitecode[i], Online
            Invcode = ' '.join(str(i) for i in Invcode)
            Invcode = Invcode.replace(' ', '').replace('.0', '')
            for q in range(len(FS100)):
                if (FS100[q][0]) == (data):
                    NightPower.append(FS100[q][1]+'_'+data+'_'+FS100[q][2]+Invcode + '\n')
    num = len(NightPower)
    print(NightPower)
    if num <= 0:
        message = "Inverter皆無ErrorCode"
        lineNotifyMessage(token, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('Inverter有ErrorCode案場'+str(num)+'場'+'\n'), sorted(NightPower)))
        lineNotifyMessage(token, message)

StartTime = '09:00:00'
EndTime = '09:00:00'
NightPower = []
sitenum = []
NightPowerError =[]
k = 0
#print(Today)
data = []
sitecode = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode.append(f.readline().replace('\n', ''))
        sql7 = "%s%s.%s '%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode[i], 'T1_head where DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
        sql8 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        cursor1 = mydb.cursor()
        cursor1.execute(sql7)
        Online = cursor1.fetchall()
        cursor2 = mydb.cursor()
        cursor2.execute(sql8)
        FS100 = cursor2.fetchall()
        if not Online:
            pass

        elif Online[0][0] < 285 or Online[0][0] > 300:
            data, count = sitecode[i], Online[0][0]
            for q in range(len(FS100)):
                if (FS100[q][0]) == (data):
                    NightPower.append(FS100[q][1]+'_'+data + '_' + str(count) + '\n')
        else:
            pass
    num = len(NightPower)
    print(NightPower)
    if num <= 0:
        message = "Count<285 or Count>300_全案場正常"
        lineNotifyMessage(token, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('Count<285 or Count>300案場'+str(num)+'場'+'\n'), sorted(NightPower)))
        lineNotifyMessage(token, message)

data = []
StartTime = '10:00:00'
EndTime = '10:00:00'
NightPower = []
sitenum = []
NightPowerError =[]
k = 0
#print(Today)

sitecode = []

with open(r'C:\_Phil\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode.append(f.readline().replace('\n', ''))
        sql9 = "%s%s.%s %s'%s'%s" % ('SELECT INVID FROM FSLG_', sitecode[i], 'T2_inv where INVXX08 > 100000', 'and DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
        sql10 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        cursor1 = mydb.cursor()
        cursor1.execute(sql9)
        Online = cursor1.fetchall()
        cursor2 = mydb.cursor()
        cursor2.execute(sql10)
        FS100 = cursor2.fetchall()
        if not Online:
            pass
        else:
            data, Invcode = sitecode[i], Online
            Invcode = ' '.join(str(i) for i in Invcode)
            Invcode = Invcode.replace('(', '').replace(',', '').replace(')', '')
            for q in range(len(FS100)):
                if (FS100[q][0]) == (data):
                    NightPower.append(FS100[q][1]+'_'+data + '_' + Invcode + '\n')
    num = len(NightPower)
    print(NightPower)
    if num <= 0:
        message = "Inveter發電量未有超過十萬案場"
        lineNotifyMessage(token, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('Inveter發電量超過十萬案場'+str(num)+'場'+'\n'), sorted(NightPower)))
        lineNotifyMessage(token, message)

data = []
StartTime = '06:00:00'
EndTime = '18:00:00'
NightPower = []
sitenum = []
NightPowerError =[]
k = 0
#print(Today)


sitecode = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode.append(f.readline().replace('\n', ''))
        sql11 = "%s%s.%s '%s'%s'%s'%s'%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode[i], 'T2_inv where invid = 1 and DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(), 1),', '%Y/%m/%d', ')) and DAQ_Time >= ', StartTime, ' AND DAQ_Time < ', EndTime, ' GROUP BY daq_date')
        sql12 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        print(sql1)
        cursor1 = mydb.cursor()
        cursor1.execute(sql11)
        Online = cursor1.fetchall()
        cursor2 = mydb.cursor()
        cursor2.execute(sql12)
        FS100 = cursor2.fetchall()
        if not Online:
            pass

        elif Online[0][0] < 140:
            data, count = sitecode[i], Online[0][0]
            for q in range(len(FS100)):
                if (FS100[q][0]) == (data):
                    NightPower.append(FS100[q][1]+'_'+data + '_' + str(count) + '\n')
        elif Online[0][0] > 145:
            data, count = sitecode[i], Online[0][0]
            for q in range(len(FS100)):
                if (FS100[q][0]) == (data):
                    NightPower.append(FS100[q][1]+'_'+data + '_' + str(count) + '\n')
        else:
            pass
    num = len(NightPower)
    print(NightPower)
    if num <= 0:
        message = "145>Count<140_全案場正常"
        lineNotifyMessage(token, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('145>Count<140案場'+str(num)+'場'+'\n'), sorted(NightPower)))
        lineNotifyMessage(token, message)
