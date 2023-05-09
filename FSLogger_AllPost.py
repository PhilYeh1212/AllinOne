import time
import requests
import mysql.connector
#aUGMBQKt3BvG82Ymd0jcrnI6Ec9HxRZ6UxGCsglndeB
token = '4cwTgoUM0Npnnob1D0aUHCYWxN6huiqVF9poI0G1Efe'
token1 = 'm5BLQpAdN59r03HqH1F0DjhOi9kqFqeL2Viz9n0JYvb'
token2 = '9qRjDI2UAvc2GjNHHUQLaOQKTboxm8mSa5siXPOr7Uh'
token3 = 'SyWs1WJYP64Navfp896JYMkaCItDzO8aBJxkDG6HvCH'
token4 = 'GRN2u7qcUOMphlLnNqydNiILFDYOPOaEUo3XSY88A9a'
token5 = 'WtTLOaHA3CWakWsLSoXJuU5obFNRcjZC3Cu706nWsYJ'
token6 = '6xVzbySPonIyGFgaMIwWcmuY3nNZJVIswFKp57xDCri'
token7 = '1DHgUiZ1P7iOD68qlYVSWD1AwWp2iXZYFFA5KKIA9Tl'

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code
# 自檢1
Notupload = []
mydb = mysql.connector.connect(host="35.221.247.182", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d', time.localtime())
sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
cursor1 = mydb.cursor()
cursor1.execute(sql1)
Online = cursor1.fetchall()
for k in Online:
    Extel_code = k
    Notupload.append(Extel_code[0])
num1 = len(Notupload)
if num1 <= 0:
    message = "案場正常上傳"
    lineNotifyMessage(token1, message)
if num1 > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = ((('未正常上傳案場共'+str(num1)+'場'), sorted(Notupload)))
    lineNotifyMessage(token1, message)
# 自檢2
StartTime = '00:00:00'
EndTime = '05:00:00'
data2 = []
NightPower = []
NightPower1 = []
NightPowerError =[]
k = 0
sitecode2 = []
with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode2.append(f.readline().replace('\n', ''))
        sql2 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode2[i], 'T2_inv where INVXX08 > 100', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        print(sql2)
        sql3 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        cursor2 = mydb.cursor()
        cursor2.execute(sql2)
        night = cursor2.fetchall()
        if not night:
            pass
        else:
            data2 = sitecode2[i]
            NightPower.append(data2)
    cursor2 = mydb.cursor()
    cursor2.execute(sql3)
    FS1002 = cursor2.fetchall()
    for q in range(len(FS1002)):
        for w in range(len(NightPower)):
            if (FS1002[q][0] == NightPower[w]):
                NightPower1.append(FS1002[q])
    while k < len(NightPower1):
        NightPowerError.append(NightPower1[k][1])
        k = k + 1

    num2 = len(NightPowerError)

    if num2 <= 0:
        message = "無夜間Power"
        lineNotifyMessage(token2, message)
    if num2 > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('夜間Inverter有讀值案場'+str(num2)+'場'), sorted(NightPowerError)))
        lineNotifyMessage(token2, message)

# 自檢3
Zero = []
#sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
sql4 = "SELECT Extel_code FROM FS_Logger_Global.Site_list where Instant_Power = 0"
cursor3 = mydb.cursor()
cursor3.execute(sql4)
Zerodata = cursor3.fetchall()
print(Zerodata)

for k in Zerodata:
    Extel_code = k
    Zero.append(Extel_code[0])

num3 = len(Zero)

if num3 <= 0:
    message = "案場正常發電"
    lineNotifyMessage(token3, message)
if num3 > 0:
    #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
    message = (((' Inverter發電量為零的案場共'+str(num3)+'台'), sorted(Zero)))
    lineNotifyMessage(token3, message)

# 自檢4
StartTime = '10:00:00'
EndTime = '10:00:00'
InverterError = []
k = 0
#print(Today)
data4 = []
sitecode4 = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0, 100):
        sitecode4.append(f.readline().replace('\n', ''))
        sql5 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID, INVXX02, INVXX03 FROM FSLG_', sitecode4[i], 'T2_inv where (INVXX02 > 0 or INVXX03 > 0 and INVXX03 < 100) ' , 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        print(sql5)
        sql6 = "SELECT Site_code, Extel_code, inverter FROM FS_Logger_Global.Site_list"
        cursor4 = mydb.cursor()
        cursor4.execute(sql5)
        InverterErrorCode = cursor4.fetchall()
        cursor5 = mydb.cursor()
        cursor5.execute(sql6)
        FS1004 = cursor5.fetchall()
        if not InverterErrorCode:
            pass
        else:
            data4, Invcode = sitecode4[i], InverterErrorCode
            Invcode = ' '.join(str(i) for i in Invcode)
            Invcode = Invcode.replace(' ', '').replace('.0', '')
            for q in range(len(FS1004)):
                if (FS1004[q][0]) == (data4):
                    InverterError.append(FS1004[q][1]+'_'+data4+'_'+FS1004[q][2]+Invcode + '\n')
    num4 = len(InverterError)
    print(InverterError)
    if num4 <= 0:
        message = "Inverter皆無ErrorCode"
        lineNotifyMessage(token4, message)
    if num4 > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('Inverter有ErrorCode案場'+str(num4)+'場'+'\n'), sorted(InverterError)))
        lineNotifyMessage(token4, message)

# 自檢5
StartTime = '09:00:00'
EndTime = '09:00:00'
Count300 = []
k = 0
#print(Today)
data5 = []
sitecode5 = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode5.append(f.readline().replace('\n', ''))
        sql7 = "%s%s.%s '%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode5[i], 'T1_head where DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
        print(sql7)
        sql8 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        cursor6 = mydb.cursor()
        cursor6.execute(sql7)
        Count285 = cursor6.fetchall()
        cursor7 = mydb.cursor()
        cursor7.execute(sql8)
        FS1005 = cursor7.fetchall()
        if not Count285:
            pass
        elif Count285[0][0] < 285 or Count285[0][0] > 300:
            data5, count = sitecode5[i], Count285[0][0]
            for q in range(len(FS1005)):
                if (FS1005[q][0]) == (data5):
                    Count300.append(FS1005[q][1]+'_'+data5 + '_' + str(count) + '\n')
        else:
            pass
    num5 = len(Count300)
    print(Count300)
    if num5 <= 0:
        message = "Count<285 or Count>300_全案場正常"
        lineNotifyMessage(token5, message)
    if num5 > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('Count<285 or Count>300案場'+str(num5)+'場'+'\n'), sorted(Count300)))
        lineNotifyMessage(token5, message)

data6 = []
StartTime = '10:00:00'
EndTime = '10:00:00'
Inverter10000 = []
k = 0
#print(Today)

sitecode6 = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode6.append(f.readline().replace('\n', ''))
        sql9 = "%s%s.%s %s'%s'%s" % ('SELECT INVID FROM FSLG_', sitecode6[i], 'T2_inv where INVXX08 > 100000', 'and DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
        print(sql9)
        sql10 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        cursor8 = mydb.cursor()
        cursor8.execute(sql9)
        Inverterover = cursor8.fetchall()
        cursor9 = mydb.cursor()
        cursor9.execute(sql10)
        FS1006 = cursor9.fetchall()
        if not Inverterover:
            pass
        else:
            data6, Invcode = sitecode6[i], Inverterover
            Invcode = ' '.join(str(i) for i in Invcode)
            Invcode = Invcode.replace('(', '').replace(',', '').replace(')', '')
            for q in range(len(FS1006)):
                if (FS1006[q][0]) == (data6):
                    Inverter10000.append(FS1006[q][1]+'_'+data6 + '_' + Invcode + '\n')
    num = len(Inverter10000)
    print(Inverter10000)
    if num <= 0:
        message = "Inveter發電量未有超過十萬案場"
        lineNotifyMessage(token6, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('Inveter發電量超過十萬案場'+str(num)+'場'+'\n'), sorted(Inverter10000)))
        lineNotifyMessage(token6, message)
# 自檢7
data7 = []
StartTime = '06:00:00'
EndTime = '18:00:00'
Count140 = []

k = 0
#print(Today)


sitecode = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode.append(f.readline().replace('\n', ''))
        sql11 = "%s%s.%s '%s'%s'%s'%s'%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode[i], 'T2_inv where invid = 1 and DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(), 1),', '%Y/%m/%d', ')) and DAQ_Time >= ', StartTime, ' AND DAQ_Time < ', EndTime, ' GROUP BY daq_date')
        print(sql11)
        sql12 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        print(sql1)
        cursor10 = mydb.cursor()
        cursor10.execute(sql11)
        Count145 = cursor10.fetchall()
        cursor11 = mydb.cursor()
        cursor11.execute(sql12)
        FS1007 = cursor11.fetchall()
        if not Count145:
            pass

        elif Count145[0][0] < 140:
            data7, count = sitecode[i], Count145[0][0]
            for q in range(len(FS1007)):
                if (FS1007[q][0]) == (data7):
                    Count140.append(FS1007[q][1]+'_'+data7 + '_' + str(count) + '\n')
        elif Count145[0][0] > 145:
            data7, count = sitecode[i], Count145[0][0]
            for q in range(len(FS1007)):
                if (FS1007[q][0]) == (data7):
                    Count140.append(FS1007[q][1]+'_'+data7 + '_' + str(count) + '\n')
        else:
            pass
    num = len(Count140)
    print(Count140)
    if num <= 0:
        message = "145>Count<140_全案場正常"
        lineNotifyMessage(token7, message)
    if num > 0:
        #message = '%s\n%s:%s%s:%s\n%s:%s' % ('\n缺資料機台', 'Date', date1, 'ID', DAS1, 'Count', Count1)
        message = ((('145>Count<140案場'+str(num)+'場'+'\n'), sorted(Count140)))
        lineNotifyMessage(token7, message)
