import time
import requests
import mysql.connector

#3aFS6TkETYwlVEW5IkWKrJ5Mkv1IeV2Zc1AQCB393pI --Extel內部群
token = 'dm2P7JE3RIUpfkMaRHvMIAeFXEiFFElRSF7LOJN6NtE' #extel工程部

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

#mydb = mysql.connector.connect(host="localhost",user="root",passwd="Oerlikon;1234",)
#mydb = mysql.connector.connect(host="35.236.181.75", user="Phil", password="Qwe751212", port=3306)
mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d', time.localtime())
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
        sql1 = "%s%s.%s %s'%s'%s'%s'%s'%s'" % ('SELECT INVID FROM FSLG_', sitecode[i], 'T2_inv where INVXX08 > 100', 'and DAQ_DAte =', Today,' and DAQ_Time BETWEEN ', StartTime, ' AND ', EndTime)
        sql2 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        #sql1 = "SELECT Extel_code FROM FS_Logger_Global.Site_list where Instant_Power = 0"

        cursor1 = mydb.cursor()
        cursor1.execute(sql1)
        Online = cursor1.fetchall()
        if not Online:
            pass
        else:
            data = sitecode[i]
            NightPower.append(data)
    cursor2 = mydb.cursor()
    cursor2.execute(sql2)
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
