import time
import requests
import mysql.connector

#A5Yk905AM8Dw7ct7jqMf3u59d0xEVy3xp19hYYwCsXv --extel內部群
token = 'A5Yk905AM8Dw7ct7jqMf3u59d0xEVy3xp19hYYwCsXv'

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
data = []
mydb = mysql.connector.connect(host="localhost", user="root", password="Oerlikon;1234", port=3306, database="FS_Logger_Global")
Today = time.strftime('%Y/%m/%d', time.localtime())
StartTime = '09:00:00'
EndTime = '09:00:00'
NightPower = []
sitenum = []
NightPowerError =[]
k = 0
#print(Today)

sitecode = []

with open(r'C:\FS100.txt', 'r') as f:
    for i in range(0,100):
        sitecode.append(f.readline().replace('\n', ''))
        #sql1 = "%s'%s'" % ('SELECT Extel_code FROM FS_Logger_Global.Site_list where DAQ_DAte != ', Today)
        sql1 = "%s%s.%s '%s'%s" % ('SELECT count(DAQ_Date) FROM FSLG_', sitecode[i], 'T1_head where DAQ_Date = (SELECT DATE_FORMAT(subdate(CURDATE(),1),','%Y/%m/%d', '))')
        sql2 = "SELECT Site_code, Extel_code FROM FS_Logger_Global.Site_list"
        #sql1 = "SELECT Extel_code FROM FS_Logger_Global.Site_list where Instant_Power = 0"
        print(sql1)
        cursor1 = mydb.cursor()
        cursor1.execute(sql1)
        Online = cursor1.fetchall()
        cursor2 = mydb.cursor()
        cursor2.execute(sql2)
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
